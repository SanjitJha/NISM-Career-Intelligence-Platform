import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from database.db_connection import execute_query


def render():
    st.title("📈 Analytics Dashboard")

    # ── Jobs by City ───────────────────────────────────────────
    city_data = execute_query("""
        SELECT location, COUNT(*) AS job_count
        FROM jobs WHERE is_active=1 AND location != ''
        GROUP BY location ORDER BY job_count DESC LIMIT 10
    """, fetch=True)

    if city_data:
        df_city = pd.DataFrame(city_data)
        fig1 = px.bar(df_city, x="location", y="job_count",
                      title="Top 10 Cities by Job Count",
                      color="job_count", color_continuous_scale="Blues")
        st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    # ── NISM vs Non-NISM ──────────────────────────────────────
    with col1:
        nism_data = execute_query("""
            SELECT
                CASE WHEN nism_required=1 THEN 'NISM Required' ELSE 'Not Required' END AS label,
                COUNT(*) AS count
            FROM jobs WHERE is_active=1 GROUP BY nism_required
        """, fetch=True)
        if nism_data:
            df_nism = pd.DataFrame(nism_data)
            fig2 = px.pie(df_nism, names="label", values="count",
                          title="NISM Certification Requirement",
                          color_discrete_sequence=["#1565C0", "#90CAF9"])
            st.plotly_chart(fig2, use_container_width=True)

    # ── Jobs by Source ────────────────────────────────────────
    with col2:
        src_data = execute_query("""
            SELECT source, COUNT(*) AS count
            FROM jobs WHERE is_active=1
            GROUP BY source ORDER BY count DESC
        """, fetch=True)
        if src_data:
            df_src = pd.DataFrame(src_data)
            fig3 = px.pie(df_src, names="source", values="count",
                          title="Jobs by Source Platform")
            st.plotly_chart(fig3, use_container_width=True)

    # ── Relevance Score Distribution ─────────────────────────
    score_data = execute_query("""
        SELECT relevance_score FROM jobs WHERE is_active=1
    """, fetch=True)
    if score_data:
        df_score = pd.DataFrame(score_data)
        fig4 = px.histogram(df_score, x="relevance_score", nbins=10,
                            title="Relevance Score Distribution",
                            color_discrete_sequence=["#1565C0"])
        st.plotly_chart(fig4, use_container_width=True)
