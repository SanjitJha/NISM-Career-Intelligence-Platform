"""
Transformer — cleans raw records and computes relevance scores.
Input:  list of raw dicts
Output: list of clean dicts ready for DB insert
"""
import re
from datetime import date
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import NISM_KEYWORDS
from loguru import logger


def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r'\s+', ' ', str(text).strip())


def detect_nism_required(text: str) -> bool:
    """Return True if NISM or related keywords appear in the text."""
    text_lower = text.lower()
    triggers = ["nism", "amfi", "sebi certified", "nism series", "nism certification"]
    return any(kw in text_lower for kw in triggers)


def compute_relevance_score(record: dict) -> int:
    """
    Score 0–100 based on:
      40 pts — nism_required flag
      30 pts — keyword in position title
      20 pts — keyword in job description
      10 pts — posted within last 14 days
    """
    score = 0
    position    = (record.get("position")        or "").lower()
    description = (record.get("job_description") or "").lower()

    if record.get("nism_required"):
        score += 40

    kw_lower = [k.lower() for k in NISM_KEYWORDS]
    if any(kw in position for kw in kw_lower):
        score += 30
    if any(kw in description for kw in kw_lower):
        score += 20

    posted = record.get("posted_date")
    if posted:
        try:
            delta = (date.today() - date.fromisoformat(str(posted))).days
            if delta <= 14:
                score += 10
        except ValueError:
            pass

    return min(score, 100)


def transform(raw_records: list[dict]) -> list[dict]:
    """
    Clean and enrich every raw record.
    Skips records missing both company_name and position.
    """
    cleaned = []
    skipped = 0

    for raw in raw_records:
        company  = clean_text(raw.get("company_name") or raw.get("company"))
        position = clean_text(raw.get("position")     or raw.get("title"))

        if not company and not position:
            skipped += 1
            continue

        description = clean_text(raw.get("job_description") or raw.get("description") or "")
        combined    = f"{position} {description}"

        record = {
            "company_name":        company,
            "position":            position,
            "salary":              clean_text(raw.get("salary") or "Not Disclosed"),
            "location":            clean_text(raw.get("location") or ""),
            "experience_required": clean_text(raw.get("experience_required") or raw.get("experience") or ""),
            "nism_required":       detect_nism_required(combined),
            "source":              clean_text(raw.get("source") or "Unknown"),
            "apply_link":          (raw.get("apply_link") or raw.get("url") or "").strip(),
            "job_description":     description,
            "posted_date":         raw.get("posted_date") or str(date.today()),
        }
        record["relevance_score"] = compute_relevance_score(record)
        cleaned.append(record)

    logger.info(f"[Transformer] {len(cleaned)} records cleaned, {skipped} skipped")
    return cleaned
