import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from database.db_connection import execute_query


def render():
    st.title("📋 Weekly Reports")

    history = execute_query("""
        SELECT week_start, total_jobs, new_jobs_this_week,
               total_companies, nism_required_jobs,
               top_city, avg_relevance_score
        FROM weekly_stats ORDER BY week_start DESC
    """, fetch=True)

    if history:
        st.dataframe(pd.DataFrame(history), use_container_width=True)
    else:
        st.info("No weekly stats yet. Run the ETL pipeline to generate them.")

    st.divider()
    st.subheader("⬇️  Export Data")
    col1, col2 = st.columns(2)
    with col1:
        jobs = execute_query("SELECT * FROM jobs WHERE is_active=1", fetch=True)
        if jobs:
            df = pd.DataFrame(jobs)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Jobs CSV", csv, "jobs_export.csv", "text/csv")
    with col2:
        st.button("📧 Send Email Report", help="Configure email in config/config.py first")
