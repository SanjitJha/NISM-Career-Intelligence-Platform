"""
Streamlit entry point — run with: streamlit run dashboard/app.py
"""
import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import APP_TITLE, APP_ICON, APP_LAYOUT

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded",
)

# ── Sidebar navigation ─────────────────────────────────────
st.sidebar.title("📊 NISM Job Tracker")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to",
    ["🏠 Overview", "💼 Job Listings", "📈 Analytics", "📋 Reports"],
)

# ── Route to pages ──────────────────────────────────────────
if page == "🏠 Overview":
    from dashboard.pages import overview
    overview.render()
elif page == "💼 Job Listings":
    from dashboard.pages import jobs
    jobs.render()
elif page == "📈 Analytics":
    from dashboard.pages import analytics
    analytics.render()
elif page == "📋 Reports":
    from dashboard.pages import reports
    reports.render()

st.sidebar.markdown("---")
st.sidebar.caption("NISM Career Intelligence Platform v1.0")
