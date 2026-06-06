"""
scraper/naukri_jobs.py
──────────────────────
Naukri.com scraper for NISM-related finance jobs.

IMPORTANT — run this on YOUR LOCAL MACHINE, not this sandbox.
This sandbox's network only allows package-registry traffic.
On your laptop: python scraper/naukri_jobs.py

How it works
────────────
Naukri renders job cards server-side.  We:
  1. Build a search URL (keyword + location)
  2. GET the page with browser-like headers + a session cookie
  3. Parse job cards with BeautifulSoup
  4. Save raw JSON to data/raw/  for the ETL pipeline to process

Anti-bot notes
──────────────
• Always add a random 2–4 s delay between pages  (polite scraping)
• Rotate User-Agent strings from the pool below
• Re-use a requests.Session() so cookies persist across pages
• If you hit a CAPTCHA, stop immediately — do not retry in a loop
• Naukri's ToS: scraping is for personal/research use only
"""

import time
import random
import json
import re
import sys
import os
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup

# ── project root on sys.path ────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import (
    REQUEST_TIMEOUT, DATA_RAW_PATH,
    NISM_KEYWORDS,
)
from loguru import logger

# ───────────────────────────────────────────────────────────────
# CONSTANTS
# ───────────────────────────────────────────────────────────────
BASE_URL    = "https://www.naukri.com"
SEARCH_URL  = "https://www.naukri.com/{keyword}-jobs-{page}"   # e.g. nism-jobs-1
MAX_PAGES   = 5          # stop after this many result pages
MIN_DELAY   = 2.0        # seconds between requests (min)
MAX_DELAY   = 4.5        # seconds between requests (max)
SOURCE_LABEL = "Naukri"

# Rotate these to avoid fingerprinting
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# Search keywords to cycle through
SEARCH_KEYWORDS = [
    "nism",
    "nism-certified",
    "mutual-fund-advisor",
    "equity-research-analyst",
    "wealth-management",
    "sebi-registered",
    "amfi-certified",
]

# ───────────────────────────────────────────────────────────────
# SESSION SETUP
# ───────────────────────────────────────────────────────────────
def _make_session() -> requests.Session:
    """Return a session pre-loaded with browser-like headers."""
    session = requests.Session()
    session.headers.update({
        "User-Agent":       random.choice(USER_AGENTS),
        "Accept":           "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language":  "en-IN,en-GB;q=0.9,en;q=0.8",
        "Accept-Encoding":  "gzip, deflate, br",
        "DNT":              "1",
        "Connection":       "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest":   "document",
        "Sec-Fetch-Mode":   "navigate",
        "Sec-Fetch-Site":   "none",
        "Sec-Fetch-User":   "?1",
        "Cache-Control":    "max-age=0",
    })
    return session


def _polite_delay():
    """Sleep a random amount between MIN_DELAY and MAX_DELAY."""
    secs = random.uniform(MIN_DELAY, MAX_DELAY)
    logger.debug(f"[Naukri] Sleeping {secs:.1f}s...")
    time.sleep(secs)


# ───────────────────────────────────────────────────────────────
# HTML PARSERS
# ───────────────────────────────────────────────────────────────
def _safe_text(tag, selector: str, attr: str = None) -> str:
    """Extract text (or an attribute) from a CSS-selected element. Returns '' on miss."""
    el = tag.select_one(selector)
    if el is None:
        return ""
    if attr:
        return (el.get(attr) or "").strip()
    return el.get_text(separator=" ", strip=True)


def _parse_job_card(card) -> dict | None:
    """
    Parse a single Naukri job card <article> element.

    Naukri's HTML class names (as of early 2024):
      article.jobTuple          → wrapper
      a.title                   → position + URL
      a.subTitle                → company name
      span.loc.fleft            → location
      span.experience.fleft     → experience
      span.salary               → salary
      li.tag.fleft              → skill tags
      span.date                 → posted date

    ⚠️  Naukri changes class names regularly.
        If parsing breaks, open the page in DevTools (F12),
        inspect a job card, update the selectors below.
    """
    try:
        # Position + apply URL
        title_tag = card.select_one("a.title") or card.select_one("a.jobTitle")
        if title_tag is None:
            return None

        position  = title_tag.get_text(strip=True)
        apply_link = title_tag.get("href", "")
        if apply_link and not apply_link.startswith("http"):
            apply_link = BASE_URL + apply_link

        # Company
        company = _safe_text(card, "a.subTitle") or _safe_text(card, "a.companyName")

        # Location — may contain multiple spans
        location_el = card.select_one("span.loc") or card.select_one("span.location")
        location = location_el.get_text(separator=", ", strip=True) if location_el else ""

        # Experience
        experience = (
            _safe_text(card, "span.experience")
            or _safe_text(card, "span.exp")
            or ""
        )

        # Salary
        salary = (
            _safe_text(card, "span.salary")
            or _safe_text(card, "span.sal")
            or "Not Disclosed"
        )

        # Description / skill tags (join li.tag items)
        tags = [li.get_text(strip=True) for li in card.select("li.tag")]
        description = ", ".join(tags) if tags else _safe_text(card, "span.job-description")

        # Posted date
        posted_raw = _safe_text(card, "span.date") or _safe_text(card, "span.postedDate")
        posted_date = _normalise_date(posted_raw)

        if not position or not company:
            return None

        return {
            "company_name":        company,
            "position":            position,
            "salary":              salary,
            "location":            location,
            "experience_required": experience,
            "source":              SOURCE_LABEL,
            "apply_link":          apply_link,
            "job_description":     description,
            "posted_date":         posted_date,
        }

    except Exception as e:
        logger.warning(f"[Naukri] Card parse error: {e}")
        return None


def _normalise_date(raw: str) -> str:
    """
    Convert Naukri date strings to ISO YYYY-MM-DD.
    Examples: '15 Jan 2024', 'Just now', '3 Days Ago', 'Today'
    """
    if not raw:
        return str(date.today())

    raw_lower = raw.lower().strip()

    if "just now" in raw_lower or "today" in raw_lower or "few hours" in raw_lower:
        return str(date.today())

    m = re.search(r"(\d+)\s+day", raw_lower)
    if m:
        from datetime import timedelta
        return str(date.today() - timedelta(days=int(m.group(1))))

    m = re.search(r"(\d+)\s+month", raw_lower)
    if m:
        from datetime import timedelta
        return str(date.today() - timedelta(days=int(m.group(1)) * 30))

    # Try standard formats
    for fmt in ("%d %b %Y", "%d %B %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).date().isoformat()
        except ValueError:
            pass

    return str(date.today())


# ───────────────────────────────────────────────────────────────
# PAGE FETCHER
# ───────────────────────────────────────────────────────────────
def _fetch_page(session: requests.Session, url: str) -> BeautifulSoup | None:
    """GET one URL and return parsed soup, or None on failure."""
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            logger.info(f"[Naukri] ✅ {resp.status_code} {url}")
            return BeautifulSoup(resp.text, "html.parser")
        elif resp.status_code == 429:
            logger.warning("[Naukri] 429 Rate Limited — sleeping 60s then retrying once")
            time.sleep(60)
            resp = session.get(url, timeout=REQUEST_TIMEOUT)
            return BeautifulSoup(resp.text, "html.parser") if resp.status_code == 200 else None
        else:
            logger.warning(f"[Naukri] ❌ {resp.status_code} {url}")
            return None
    except requests.RequestException as e:
        logger.error(f"[Naukri] Request failed for {url}: {e}")
        return None


# ───────────────────────────────────────────────────────────────
# MAIN SCRAPER
# ───────────────────────────────────────────────────────────────
def scrape_keyword(keyword: str, max_pages: int = MAX_PAGES) -> list[dict]:
    """
    Scrape all result pages for a single keyword.
    Returns a list of raw job dicts.
    """
    session = _make_session()
    jobs    = []
    seen_links = set()   # deduplicate within this run

    for page_num in range(1, max_pages + 1):
        # Naukri page-1 URL has no suffix; page-2+ appends the number
        if page_num == 1:
            url = f"{BASE_URL}/{keyword}-jobs"
        else:
            url = f"{BASE_URL}/{keyword}-jobs-{page_num}"

        soup = _fetch_page(session, url)
        if soup is None:
            logger.warning(f"[Naukri] Stopping at page {page_num} — failed to fetch")
            break

        # Check for CAPTCHA or bot-detection redirect
        page_title = soup.title.string if soup.title else ""
        if "captcha" in page_title.lower() or "robot" in page_title.lower():
            logger.error("[Naukri] ⚠️  CAPTCHA detected — stopping scrape for this keyword")
            break

        # Find job cards — try multiple selector patterns
        cards = (
            soup.select("article.jobTuple")
            or soup.select("article.job-post")
            or soup.select("div.jobTuple")
            or soup.select("[class*='jobTuple']")
            or soup.select("li.type-a")
        )

        if not cards:
            logger.info(f"[Naukri] No cards on page {page_num} — may be last page")
            break

        logger.info(f"[Naukri] Page {page_num}: found {len(cards)} cards")

        for card in cards:
            job = _parse_job_card(card)
            if job is None:
                continue
            # Skip duplicates within this run
            key = (job["company_name"].lower(), job["position"].lower())
            if key in seen_links:
                continue
            seen_links.add(key)
            jobs.append(job)

        # Stop if we're on the last page (Naukri shows no "next" beyond result set)
        next_btn = soup.select_one("a[class*='next']") or soup.select_one("[aria-label='Next']")
        if next_btn is None and page_num > 1:
            logger.info("[Naukri] No 'next' button — reached last page")
            break

        _polite_delay()

    logger.info(f"[Naukri] '{keyword}': scraped {len(jobs)} jobs across {page_num} pages")
    return jobs


def scrape(
    keywords: list[str] = None,
    max_pages: int = MAX_PAGES,
    save: bool = True,
) -> list[dict]:
    """
    Public entry point — called by ETL pipeline.

    Parameters
    ----------
    keywords  : list of keyword slugs to search. Defaults to SEARCH_KEYWORDS.
    max_pages : max result pages per keyword.
    save      : if True, writes raw JSON to data/raw/.

    Returns
    -------
    list of raw job dicts (not yet transformed)
    """
    if keywords is None:
        keywords = SEARCH_KEYWORDS

    all_jobs = []
    seen = set()   # global dedup across keywords

    for kw in keywords:
        logger.info(f"[Naukri] === Searching: {kw} ===")
        jobs = scrape_keyword(kw, max_pages)

        for job in jobs:
            key = (job["company_name"].lower(), job["position"].lower())
            if key not in seen:
                seen.add(key)
                all_jobs.append(job)

        # Extra delay between keyword searches
        if kw != keywords[-1]:
            time.sleep(random.uniform(3, 6))

    logger.info(f"[Naukri] Total unique jobs scraped: {len(all_jobs)}")

    if save and all_jobs:
        os.makedirs(DATA_RAW_PATH, exist_ok=True)
        filename = f"naukri_{date.today()}.json"
        filepath = os.path.join(DATA_RAW_PATH, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=2)
        logger.info(f"[Naukri] Saved → {filepath}")

    return all_jobs


# ───────────────────────────────────────────────────────────────
# CLI entry point  — python scraper/naukri_jobs.py
# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Naukri NISM job scraper")
    parser.add_argument("--keywords", nargs="+", default=None,
                        help="Override keyword list, e.g. --keywords nism mutual-fund")
    parser.add_argument("--pages",    type=int, default=MAX_PAGES,
                        help=f"Max pages per keyword (default {MAX_PAGES})")
    parser.add_argument("--no-save",  action="store_true",
                        help="Don't write results to data/raw/")
    args = parser.parse_args()

    results = scrape(
        keywords  = args.keywords,
        max_pages = args.pages,
        save      = not args.no_save,
    )

    print(f"\n✅  Scraped {len(results)} unique jobs from Naukri")
    if results:
        print("\nSample (first 3):")
        for job in results[:3]:
            print(f"  • {job['company_name']} — {job['position']} ({job['location']})")
