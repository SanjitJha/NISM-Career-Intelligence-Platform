import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from database.db_connection import execute_query


def render():
    st.title("💼 Job Listings")

    # ── Filters ───────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        nism_only = st.checkbox("NISM Required only", value=False)
    with col2:
        min_score = st.slider("Min Relevance Score", 0, 100, 50)
    with col3:
        locations = execute_query(
            "SELECT DISTINCT location FROM jobs WHERE location != '' ORDER BY location",
            fetch=True
        )
        loc_list = ["All"] + [r["location"] for r in locations]
        selected_loc = st.selectbox("Location", loc_list)

    # ── Build query ────────────────────────────────────────────
    where_clauses = ["is_active = 1", "relevance_score >= %s"]
    params = [min_score]

    if nism_only:
        where_clauses.append("nism_required = 1")
    if selected_loc != "All":
        where_clauses.append("location = %s")
        params.append(selected_loc)

    sql = f"""
        SELECT job_id, company_name, position, location, salary,
               experience_required, nism_required, relevance_score,
               source, posted_date, apply_link
        FROM jobs
        WHERE {' AND '.join(where_clauses)}
        ORDER BY relevance_score DESC
    """
    jobs = execute_query(sql, tuple(params), fetch=True)

    st.markdown(f"**{len(jobs)} jobs found**")

    if jobs:
        df = pd.DataFrame(jobs)
        df["nism_required"] = df["nism_required"].map({1: "✅ Yes", 0: "No"})
        st.dataframe(df.drop(columns=["job_id"]), use_container_width=True)
    else:
        st.info("No jobs match the selected filters.")
