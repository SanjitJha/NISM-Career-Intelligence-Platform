import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from database.db_connection import execute_query


def render():
    st.title("🏠 Platform Overview")
    st.markdown("Real-time snapshot of NISM job market intelligence.")

    # ── KPI Cards ─────────────────────────────────────────────
    stats = execute_query("""
        SELECT
            COUNT(*)                        AS total_jobs,
            SUM(nism_required)              AS nism_jobs,
            COUNT(DISTINCT company_name)    AS companies,
            ROUND(AVG(relevance_score), 1)  AS avg_score
        FROM jobs WHERE is_active = 1
    """, fetch=True)[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Jobs",        stats["total_jobs"] or 0)
    col2.metric("NISM Required",     stats["nism_jobs"]  or 0)
    col3.metric("Companies",         stats["companies"]  or 0)
    col4.metric("Avg Relevance Score", stats["avg_score"] or 0)

    st.divider()

    # ── Recent Jobs ────────────────────────────────────────────
    st.subheader("🆕 Most Recently Scraped Jobs")
    recent = execute_query("""
        SELECT company_name, position, location, relevance_score, scraped_date
        FROM jobs WHERE is_active = 1
        ORDER BY scraped_date DESC LIMIT 10
    """, fetch=True)
    if recent:
        import pandas as pd
        st.dataframe(pd.DataFrame(recent), use_container_width=True)
    else:
        st.info("No jobs loaded yet. Run the ETL pipeline first.")
