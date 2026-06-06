"""
Generates a weekly HTML + Excel summary report from weekly_stats.
"""
import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import execute_query
from config.config import DATA_EXPORTS_PATH
from loguru import logger
from datetime import date


def generate_report() -> str:
    """Build weekly Excel report. Returns the output file path."""
    os.makedirs(DATA_EXPORTS_PATH, exist_ok=True)
    report_path = os.path.join(DATA_EXPORTS_PATH, f"weekly_report_{date.today()}.xlsx")

    jobs_df  = pd.DataFrame(execute_query("SELECT * FROM jobs WHERE is_active=1", fetch=True))
    stats_df = pd.DataFrame(execute_query("SELECT * FROM weekly_stats ORDER BY week_start DESC LIMIT 4", fetch=True))

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        jobs_df.to_excel(writer,  sheet_name="All Jobs",      index=False)
        stats_df.to_excel(writer, sheet_name="Weekly Stats",  index=False)

    logger.info(f"[Report] Saved to {report_path}")
    return report_path
