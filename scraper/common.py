"""
Shared utilities for all scrapers — headers, retry logic, delay.
"""
import time
import random
import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import REQUEST_TIMEOUT, REQUEST_DELAY, MAX_RETRIES, USER_AGENT
from loguru import logger

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch_page(url: str) -> BeautifulSoup | None:
    """GET a URL with retry logic. Returns parsed BeautifulSoup or None."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            delay = REQUEST_DELAY + random.uniform(0.5, 1.5)
            time.sleep(delay)
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.warning(f"[Scraper] Attempt {attempt}/{MAX_RETRIES} failed for {url}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(attempt * 2)
    logger.error(f"[Scraper] All attempts failed for {url}")
    return None


def save_raw(records: list[dict], filename: str):
    """Save scraped records to data/raw/ as JSON."""
    import json
    from config.config import DATA_RAW_PATH
    os.makedirs(DATA_RAW_PATH, exist_ok=True)
    path = os.path.join(DATA_RAW_PATH, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    logger.info(f"[Scraper] Saved {len(records)} records → {path}")
