"""
etl/loader.py
─────────────
Inserts clean job records into MySQL and maintains aggregate tables.

Public API:
    load_jobs(records, source_label)  → {inserted, skipped, duplicate}
    update_weekly_stats()             → upserts this week's KPI row
    upsert_company(company_name, ...)  → insert/ignore company row
"""

from datetime import date, timedelta
from typing import Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import execute_query, execute_many
from loguru import logger


# ─────────────────────────────────────────────────────────────────
# INSERT SQL
# ─────────────────────────────────────────────────────────────────

_INSERT_JOB = """
    INSERT INTO jobs (
        company_name, position,
        salary_raw, salary_min, salary_max,
        location, city,
        experience_required, exp_min_years, exp_max_years,
        nism_required, nism_series,
        source, apply_link, job_description,
        relevance_score, posted_date
    ) VALUES (
        %(company_name)s, %(position)s,
        %(salary_raw)s, %(salary_min)s, %(salary_max)s,
        %(location)s, %(city)s,
        %(experience_required)s, %(exp_min_years)s, %(exp_max_years)s,
        %(nism_required)s, %(nism_series)s,
        %(source)s, %(apply_link)s, %(job_description)s,
        %(relevance_score)s, %(posted_date)s
    )
"""

_DUPLICATE_CHECK = """
    SELECT job_id FROM jobs
    WHERE company_name = %s
      AND position     = %s
      AND posted_date  = %s
    LIMIT 1
"""


def _is_duplicate(record: dict) -> bool:
    """Return True if this exact job (company + position + date) is already in DB."""
    rows = execute_query(
        _DUPLICATE_CHECK,
        (record["company_name"], record["position"], record.get("posted_date")),
        fetch=True,
    )
    return bool(rows)


# ─────────────────────────────────────────────────────────────────
# Public: load_jobs
# ─────────────────────────────────────────────────────────────────

def load_jobs(records: list[dict], source_label: str = "ETL") -> dict:
    """
    Insert a batch of clean job dicts into the jobs table.
    Skips duplicates (same company + position + posted_date).

    Returns
    -------
    {
        "inserted":  int,   # rows successfully inserted
        "skipped":   int,   # rows that failed on DB error
        "duplicate": int,   # rows already in the DB
    }
    """
    inserted = skipped = duplicate = 0

    for record in records:
        try:
            if _is_duplicate(record):
                duplicate += 1
                logger.debug(
                    f"[Loader] Duplicate skipped: {record['company_name']} — {record['position']}"
                )
                continue
            execute_query(_INSERT_JOB, record)
            inserted += 1
        except Exception as e:
            logger.warning(
                f"[Loader] Insert failed ({record.get('position', '?')} "
                f"@ {record.get('company_name', '?')}): {e}"
            )
            skipped += 1

    logger.info(
        f"[Loader] {source_label}: "
        f"inserted={inserted}  duplicate={duplicate}  error={skipped}"
    )
    return {"inserted": inserted, "skipped": skipped, "duplicate": duplicate}


# ─────────────────────────────────────────────────────────────────
# Public: update_weekly_stats
# ─────────────────────────────────────────────────────────────────

def update_weekly_stats() -> None:
    """
    Recalculate all KPIs and upsert the weekly_stats row
    for the current ISO week (Monday as week_start).
    """
    today      = date.today()
    week_start = today - timedelta(days=today.weekday())   # Monday

    # ── aggregate queries ──────────────────────────────────────
    totals = execute_query("""
        SELECT
            COUNT(*)                          AS total_jobs,
            SUM(nism_required)                AS nism_jobs,
            ROUND(AVG(relevance_score), 2)    AS avg_score,
            COUNT(DISTINCT company_name)      AS total_companies,
            SUM(relevance_score >= 80)        AS high_score_jobs
        FROM jobs
        WHERE is_active = 1
    """, fetch=True)[0]

    top_city = (execute_query("""
        SELECT city, COUNT(*) AS cnt
        FROM jobs
        WHERE is_active = 1 AND city != ''
        GROUP BY city
        ORDER BY cnt DESC
        LIMIT 1
    """, fetch=True) or [{"city": "N/A"}])[0]["city"]

    top_pos = (execute_query("""
        SELECT position, COUNT(*) AS cnt
        FROM jobs
        WHERE is_active = 1
        GROUP BY position
        ORDER BY cnt DESC
        LIMIT 1
    """, fetch=True) or [{"position": "N/A"}])[0]["position"]

    top_src = (execute_query("""
        SELECT source, COUNT(*) AS cnt
        FROM jobs
        WHERE is_active = 1
        GROUP BY source
        ORDER BY cnt DESC
        LIMIT 1
    """, fetch=True) or [{"source": "N/A"}])[0]["source"]

    new_this_week = execute_query("""
        SELECT COUNT(*) AS cnt
        FROM jobs
        WHERE scraped_date >= %s AND is_active = 1
    """, (week_start,), fetch=True)[0]["cnt"]

    execute_query("""
        INSERT INTO weekly_stats
            (week_start, total_jobs, new_jobs_this_week, total_companies,
             nism_required_jobs, avg_relevance_score,
             top_city, top_position, top_source, high_score_jobs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            total_jobs          = VALUES(total_jobs),
            new_jobs_this_week  = VALUES(new_jobs_this_week),
            total_companies     = VALUES(total_companies),
            nism_required_jobs  = VALUES(nism_required_jobs),
            avg_relevance_score = VALUES(avg_relevance_score),
            top_city            = VALUES(top_city),
            top_position        = VALUES(top_position),
            top_source          = VALUES(top_source),
            high_score_jobs     = VALUES(high_score_jobs),
            updated_at          = NOW()
    """, (
        week_start,
        totals["total_jobs"]     or 0,
        new_this_week            or 0,
        totals["total_companies"] or 0,
        totals["nism_jobs"]      or 0,
        float(totals["avg_score"] or 0),
        top_city, top_pos, top_src,
        totals["high_score_jobs"] or 0,
    ))
    logger.info(f"[Loader] weekly_stats upserted for {week_start}")


# ─────────────────────────────────────────────────────────────────
# Public: upsert_company
# ─────────────────────────────────────────────────────────────────

def upsert_company(
    company_name: str,
    industry: Optional[str] = None,
    headquarters: Optional[str] = None,
    website: Optional[str] = None,
) -> None:
    """Insert a company if it doesn't already exist (by name)."""
    execute_query("""
        INSERT IGNORE INTO companies (company_name, industry, headquarters, website)
        VALUES (%s, %s, %s, %s)
    """, (company_name, industry, headquarters, website))
