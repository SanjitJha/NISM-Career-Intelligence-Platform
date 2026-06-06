"""
Loader — inserts clean records into MySQL and updates weekly_stats.
"""
from datetime import date, timedelta
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import execute_query, execute_many
from loguru import logger


INSERT_JOB_SQL = """
    INSERT INTO jobs
        (company_name, position, salary, location, experience_required,
         nism_required, source, apply_link, job_description,
         relevance_score, posted_date)
    VALUES
        (%(company_name)s, %(position)s, %(salary)s, %(location)s,
         %(experience_required)s, %(nism_required)s, %(source)s,
         %(apply_link)s, %(job_description)s, %(relevance_score)s,
         %(posted_date)s)
"""


def load_jobs(records: list[dict], source_label: str = "ETL") -> dict:
    """
    Insert a batch of clean job records.
    Returns { inserted, skipped } counts.
    """
    inserted = 0
    skipped  = 0

    for record in records:
        try:
            execute_query(INSERT_JOB_SQL, record)
            inserted += 1
        except Exception as e:
            logger.warning(f"[Loader] Skipped record ({record.get('position')}): {e}")
            skipped += 1

    logger.info(f"[Loader] source={source_label}  inserted={inserted}  skipped={skipped}")
    return {"inserted": inserted, "skipped": skipped}


def update_weekly_stats():
    """Recalculate and upsert the weekly_stats row for the current week."""
    week_start = date.today() - timedelta(days=date.today().weekday())

    stats = execute_query("""
        SELECT
            COUNT(*)                        AS total_jobs,
            SUM(nism_required)              AS nism_jobs,
            AVG(relevance_score)            AS avg_score,
            COUNT(DISTINCT company_name)    AS total_companies
        FROM jobs WHERE is_active = 1
    """, fetch=True)[0]

    top_city = (execute_query("""
        SELECT location, COUNT(*) AS cnt
        FROM jobs WHERE is_active = 1 AND location != ''
        GROUP BY location ORDER BY cnt DESC LIMIT 1
    """, fetch=True) or [{"location": "N/A"}])[0]["location"]

    top_pos = (execute_query("""
        SELECT position, COUNT(*) AS cnt
        FROM jobs WHERE is_active = 1
        GROUP BY position ORDER BY cnt DESC LIMIT 1
    """, fetch=True) or [{"position": "N/A"}])[0]["position"]

    new_jobs = execute_query("""
        SELECT COUNT(*) AS cnt FROM jobs
        WHERE scraped_date >= %s
    """, (week_start,), fetch=True)[0]["cnt"]

    execute_query("""
        INSERT INTO weekly_stats
            (week_start, total_jobs, new_jobs_this_week, total_companies,
             nism_required_jobs, top_city, top_position, avg_relevance_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            total_jobs          = VALUES(total_jobs),
            new_jobs_this_week  = VALUES(new_jobs_this_week),
            total_companies     = VALUES(total_companies),
            nism_required_jobs  = VALUES(nism_required_jobs),
            top_city            = VALUES(top_city),
            top_position        = VALUES(top_position),
            avg_relevance_score = VALUES(avg_relevance_score)
    """, (
        week_start,
        stats["total_jobs"],
        new_jobs,
        stats["total_companies"],
        stats["nism_jobs"] or 0,
        top_city,
        top_pos,
        round(float(stats["avg_score"] or 0), 2),
    ))
    logger.info(f"[Loader] weekly_stats updated for week starting {week_start}")
