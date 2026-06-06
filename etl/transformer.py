"""
etl/transformer.py
──────────────────
Cleans raw scraped records and computes a 0-100 relevance score.

Input  : list of raw dicts (any shape — from scraper or CSV/JSON files)
Output : list of clean dicts matching the jobs table schema exactly
"""

import re
from datetime import date, datetime
from typing import Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import NISM_KEYWORDS
from loguru import logger


# ─────────────────────────────────────────────────────────────────
# Text helpers
# ─────────────────────────────────────────────────────────────────

def _clean(text) -> str:
    """Strip, collapse whitespace, coerce to str."""
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text).strip())


def _safe_date(value) -> Optional[str]:
    """
    Normalise a posted_date value to ISO format YYYY-MM-DD string.
    Accepts: datetime, date, 'YYYY-MM-DD' string, '15 Jan 2024', '3 days ago', etc.
    Returns None if it cannot be parsed (the DB column allows NULL).
    """
    if value is None:
        return None
    if isinstance(value, (date, datetime)):
        return str(value)[:10]
    s = str(value).strip()
    # already ISO
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s
    # '15 Jan 2024'  /  'January 15, 2024'
    for fmt in ("%d %b %Y", "%d %B %Y", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    # "X days ago" / "today" / "just now"
    lower = s.lower()
    if "today" in lower or "just now" in lower or "hour" in lower:
        return str(date.today())
    m = re.search(r"(\d+)\s+day", lower)
    if m:
        from datetime import timedelta
        return str(date.today() - timedelta(days=int(m.group(1))))
    return None


# ─────────────────────────────────────────────────────────────────
# NISM / salary / experience parsers
# ─────────────────────────────────────────────────────────────────

_NISM_TRIGGERS = [
    "nism", "amfi", "sebi certified", "nism series",
    "nism certification", "ncfm", "nsdl",
]

_NISM_SERIES_RE = re.compile(
    r"(nism\s+series[\s\-]?[ivxlcdm0-9]+[\-a-z]*)",
    re.IGNORECASE,
)


def _detect_nism_required(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in _NISM_TRIGGERS)


def _extract_nism_series(text: str) -> Optional[str]:
    """Pull 'NISM Series V-A', 'Series VIII', etc. from any text."""
    matches = _NISM_SERIES_RE.findall(text)
    if not matches:
        return None
    # deduplicate, title-case
    seen = []
    for m in matches:
        m_clean = re.sub(r"\s+", " ", m.strip()).title()
        if m_clean not in seen:
            seen.append(m_clean)
    return ", ".join(seen)


_SALARY_RE = re.compile(
    r"(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*([lkm]?)\s*"
    r"(?:[-–to]+\s*(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*([lkm]?))?",
    re.IGNORECASE,
)
_MULTIPLIERS = {"l": 100_000, "k": 1_000, "m": 1_000_000, "": 1}


def _parse_salary(raw: str):
    """
    Parse salary strings like '₹6L–₹10L PA' or 'INR 8,00,000 - 12,00,000'.
    Returns (salary_min, salary_max) as annual INR floats, or (None, None).
    """
    if not raw:
        return None, None
    raw = raw.replace(",", "")
    m = _SALARY_RE.search(raw)
    if not m:
        return None, None
    try:
        lo  = float(m.group(1)) * _MULTIPLIERS.get((m.group(2) or "").lower(), 1)
        hi_str = m.group(3)
        hi  = float(hi_str) * _MULTIPLIERS.get((m.group(4) or "").lower(), 1) if hi_str else lo
        # if both < 1 000 they were probably expressed in thousands already
        if lo < 100:
            lo *= 100_000
        if hi < 100:
            hi *= 100_000
        return round(lo, 2), round(hi, 2)
    except (TypeError, ValueError):
        return None, None


_EXP_RE = re.compile(r"(\d+)\s*[-–to]+\s*(\d+)\s*(?:years?|yrs?)?", re.IGNORECASE)
_EXP_SINGLE_RE = re.compile(r"(\d+)\+?\s*(?:years?|yrs?)", re.IGNORECASE)


def _parse_experience(raw: str):
    """
    Parse experience strings like '2–4 years', '3+ years', '0-2 yrs'.
    Returns (exp_min_years, exp_max_years) as ints, or (None, None).
    """
    if not raw:
        return None, None
    m = _EXP_RE.search(raw)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = _EXP_SINGLE_RE.search(raw)
    if m:
        v = int(m.group(1))
        return v, v + 2
    lower = raw.lower()
    if "fresher" in lower or "entry" in lower or "0" in raw:
        return 0, 1
    return None, None


def _extract_city(location: str) -> str:
    """Pull the first word-group before a comma as the normalised city."""
    if not location:
        return ""
    city = location.split(",")[0].strip()
    # remove extra qualifiers like 'Greater'
    city = re.sub(r"\b(Greater|New|Old)\b\s*", "", city, flags=re.IGNORECASE).strip()
    return city


# ─────────────────────────────────────────────────────────────────
# Relevance scoring  (0–100)
# ─────────────────────────────────────────────────────────────────

def _score(record: dict) -> int:
    """
    Scoring breakdown:
      40 pts — nism_required is True
      25 pts — NISM keyword in position title
      20 pts — NISM keyword in job_description
      10 pts — posted within last 14 days
       5 pts — salary_max > ₹8L  (substantial role)
    """
    score = 0
    position    = (record.get("position")        or "").lower()
    description = (record.get("job_description") or "").lower()
    kw_lower    = [k.lower() for k in NISM_KEYWORDS]

    if record.get("nism_required"):
        score += 40
    if any(kw in position for kw in kw_lower):
        score += 25
    if any(kw in description for kw in kw_lower):
        score += 20

    posted = record.get("posted_date")
    if posted:
        try:
            delta = (date.today() - date.fromisoformat(str(posted))).days
            if 0 <= delta <= 14:
                score += 10
        except ValueError:
            pass

    sal_max = record.get("salary_max")
    if sal_max and sal_max > 800_000:
        score += 5

    return min(score, 100)


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def transform(raw_records: list[dict]) -> list[dict]:
    """
    Clean and enrich every raw record.

    Rules:
    • A record is SKIPPED if both company_name and position are empty.
    • All string fields are stripped and whitespace-collapsed.
    • salary_min / salary_max are parsed from salary_raw.
    • exp_min_years / exp_max_years are parsed from experience_required.
    • city is extracted from location.
    • nism_required is inferred from combined title + description text.
    • nism_series is extracted via regex.
    • relevance_score is computed from the cleaned record.

    Returns cleaned list ready for loader.load_jobs().
    """
    cleaned = []
    skipped = 0

    for i, raw in enumerate(raw_records):
        company  = _clean(raw.get("company_name") or raw.get("company") or "")
        position = _clean(raw.get("position") or raw.get("title") or raw.get("job_title") or "")

        if not company and not position:
            logger.debug(f"[Transformer] Record {i} skipped — missing company and position")
            skipped += 1
            continue

        location    = _clean(raw.get("location") or "")
        salary_raw  = _clean(raw.get("salary") or raw.get("salary_raw") or "Not Disclosed")
        experience  = _clean(raw.get("experience_required") or raw.get("experience") or "")
        description = _clean(raw.get("job_description") or raw.get("description") or "")
        combined    = f"{position} {description}"

        sal_min, sal_max = _parse_salary(salary_raw)
        exp_min, exp_max = _parse_experience(experience)
        nism_req         = _detect_nism_required(combined)
        nism_series      = _extract_nism_series(combined) if nism_req else None

        record = {
            "company_name":        company,
            "position":            position,
            "salary_raw":          salary_raw,
            "salary_min":          sal_min,
            "salary_max":          sal_max,
            "location":            location,
            "city":                _extract_city(location),
            "experience_required": experience,
            "exp_min_years":       exp_min,
            "exp_max_years":       exp_max,
            "nism_required":       nism_req,
            "nism_series":         nism_series,
            "source":              _clean(raw.get("source") or "Unknown"),
            "apply_link":          (raw.get("apply_link") or raw.get("url") or "").strip(),
            "job_description":     description,
            "posted_date":         _safe_date(raw.get("posted_date")) or str(date.today()),
        }
        record["relevance_score"] = _score(record)
        cleaned.append(record)

    logger.info(
        f"[Transformer] Input={len(raw_records)}  "
        f"Cleaned={len(cleaned)}  Skipped={skipped}"
    )
    return cleaned
