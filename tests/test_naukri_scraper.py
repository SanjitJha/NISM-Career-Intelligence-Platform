"""
Unit tests for naukri_jobs.py — all tests run offline (no HTTP calls).
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scraper.naukri_jobs import _normalise_date, _parse_job_card
from bs4 import BeautifulSoup
from datetime import date, timedelta


# ── _normalise_date ──────────────────────────────────────────
def test_today_variants():
    for val in ["Just now", "Today", "Few hours ago"]:
        assert _normalise_date(val) == str(date.today())

def test_days_ago():
    result = _normalise_date("3 Days Ago")
    expected = str(date.today() - timedelta(days=3))
    assert result == expected

def test_month_ago():
    result = _normalise_date("1 Month Ago")
    expected = str(date.today() - timedelta(days=30))
    assert result == expected

def test_iso_passthrough():
    assert _normalise_date("15 Jan 2024") == "2024-01-15"

def test_empty_returns_today():
    assert _normalise_date("") == str(date.today())
    assert _normalise_date(None) == str(date.today())


# ── _parse_job_card ──────────────────────────────────────────
def _make_card(html: str):
    return BeautifulSoup(html, "html.parser")

def test_parse_valid_card():
    html = """
    <article class="jobTuple">
      <a class="title" href="/job-detail/12345">Research Analyst</a>
      <a class="subTitle">HDFC AMC</a>
      <span class="loc">Mumbai, Maharashtra</span>
      <span class="experience">2-4 Years</span>
      <span class="salary">₹6L–₹10L PA</span>
      <ul><li class="tag">NISM</li><li class="tag">Equity</li></ul>
      <span class="date">2 Days Ago</span>
    </article>
    """
    card = _make_card(html)
    job = _parse_job_card(card)

    assert job is not None
    assert job["position"] == "Research Analyst"
    assert job["company_name"] == "HDFC AMC"
    assert "Mumbai" in job["location"]
    assert job["experience_required"] == "2-4 Years"
    assert "6L" in job["salary"]
    assert "NISM" in job["job_description"]
    assert job["apply_link"].endswith("/job-detail/12345")
    assert job["source"] == "Naukri"

def test_parse_missing_title_returns_none():
    html = "<article class='jobTuple'><a class='subTitle'>SomeCo</a></article>"
    card = _make_card(html)
    assert _parse_job_card(card) is None

def test_parse_missing_company_returns_none():
    html = "<article class='jobTuple'><a class='title' href='/x'>Dev</a></article>"
    card = _make_card(html)
    assert _parse_job_card(card) is None

def test_apply_link_prefixed():
    html = """
    <article class="jobTuple">
      <a class="title" href="/job/999">Analyst</a>
      <a class="subTitle">TestCo</a>
    </article>"""
    job = _parse_job_card(_make_card(html))
    assert job["apply_link"].startswith("https://")

def test_salary_not_disclosed_default():
    html = """
    <article class="jobTuple">
      <a class="title" href="/job/1">Advisor</a>
      <a class="subTitle">Zerodha</a>
    </article>"""
    job = _parse_job_card(_make_card(html))
    assert job["salary"] == "Not Disclosed"
