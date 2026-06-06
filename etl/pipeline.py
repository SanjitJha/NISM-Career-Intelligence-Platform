"""
Pipeline — orchestrates Extract → Transform → Load.
Can be run directly: python etl/pipeline.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.extractor   import extract_all_raw_files, extract_from_scraper
from etl.transformer import transform
from etl.loader      import load_jobs, update_weekly_stats
from database.db_connection import execute_query
from loguru import logger
from datetime import datetime


def run_pipeline(sources: list[str] = None, use_raw_files: bool = False):
    """
    Main ETL entry point.
    sources     : ['linkedin', 'naukri', 'indeed']  — live scraping
    use_raw_files: True — process files already in data/raw/
    """
    logger.info("=" * 55)
    logger.info("  NISM Career Intelligence Platform — ETL Pipeline")
    logger.info("=" * 55)

    raw_records = []

    # ── Extract ─────────────────────────────────────────────
    if use_raw_files:
        raw_records = extract_all_raw_files()
    elif sources:
        for src in sources:
            start_log = execute_query(
                "INSERT INTO scrape_logs (source) VALUES (%s)", (src,)
            )
            try:
                records = extract_from_scraper(src)
                raw_records.extend(records)
                execute_query(
                    "UPDATE scrape_logs SET jobs_found=%s, status='success', finished_at=NOW() WHERE log_id=%s",
                    (len(records), start_log)
                )
            except Exception as e:
                logger.error(f"[Pipeline] Scraper failed for {src}: {e}")
                execute_query(
                    "UPDATE scrape_logs SET status='failed', error_message=%s, finished_at=NOW() WHERE log_id=%s",
                    (str(e), start_log)
                )

    if not raw_records:
        logger.warning("[Pipeline] No records to process. Exiting.")
        return

    # ── Transform ────────────────────────────────────────────
    clean_records = transform(raw_records)

    # ── Load ─────────────────────────────────────────────────
    result = load_jobs(clean_records)

    # ── Update weekly stats ──────────────────────────────────
    update_weekly_stats()

    logger.info(f"[Pipeline] ✅  Done — inserted={result['inserted']}  skipped={result['skipped']}")
    return result


if __name__ == "__main__":
    # Quick test: process any files already in data/raw/
    run_pipeline(use_raw_files=True)
