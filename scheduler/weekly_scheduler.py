"""
Weekly scheduler — automatically runs the ETL pipeline every Monday at 08:00.
Run as a background process: python scheduler/weekly_scheduler.py
"""
import schedule
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import SCRAPE_DAY, SCRAPE_TIME, REPORT_TIME
from etl.pipeline import run_pipeline
from reports.email_report import send_weekly_report
from loguru import logger


def run_weekly_job():
    logger.info("[Scheduler] Starting weekly scrape + ETL...")
    run_pipeline(sources=["linkedin", "naukri", "indeed"])
    logger.info("[Scheduler] Weekly ETL complete.")


def run_weekly_report():
    logger.info("[Scheduler] Sending weekly email report...")
    send_weekly_report()


# ── Schedule jobs ─────────────────────────────────────────────
getattr(schedule.every(), SCRAPE_DAY).at(SCRAPE_TIME).do(run_weekly_job)
getattr(schedule.every(), SCRAPE_DAY).at(REPORT_TIME).do(run_weekly_report)

logger.info(f"[Scheduler] Waiting... will run every {SCRAPE_DAY} at {SCRAPE_TIME}")

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
