"""
Extractor — pulls raw job data from scrapers and flat files.
All output is a list of dicts with a consistent schema.
"""
import json
import csv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DATA_RAW_PATH
from loguru import logger


def extract_from_json(filepath: str) -> list[dict]:
    """Load raw jobs from a JSON file (output from scrapers)."""
    logger.info(f"[Extractor] Reading JSON: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info(f"[Extractor] {len(data)} records loaded from JSON")
    return data


def extract_from_csv(filepath: str) -> list[dict]:
    """Load raw jobs from a CSV file."""
    logger.info(f"[Extractor] Reading CSV: {filepath}")
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    logger.info(f"[Extractor] {len(rows)} records loaded from CSV")
    return rows


def extract_from_scraper(source: str) -> list[dict]:
    """
    Dynamically call the right scraper module.
    source: 'linkedin' | 'naukri' | 'indeed'
    """
    logger.info(f"[Extractor] Triggering scraper: {source}")
    if source == "linkedin":
        from scraper.linkedin_jobs import scrape as fn
    elif source == "naukri":
        from scraper.naukri_jobs import scrape as fn
    elif source == "indeed":
        from scraper.indeed_jobs import scrape as fn
    else:
        raise ValueError(f"Unknown source: {source}")
    return fn()


def extract_all_raw_files() -> list[dict]:
    """Scan data/raw/ and load all JSON + CSV files."""
    all_records = []
    for fname in os.listdir(DATA_RAW_PATH):
        fpath = os.path.join(DATA_RAW_PATH, fname)
        if fname.endswith(".json"):
            all_records.extend(extract_from_json(fpath))
        elif fname.endswith(".csv"):
            all_records.extend(extract_from_csv(fpath))
    logger.info(f"[Extractor] Total raw records: {len(all_records)}")
    return all_records
