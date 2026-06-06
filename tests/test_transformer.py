import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from etl.transformer import clean_text, detect_nism_required, compute_relevance_score, transform


def test_clean_text():
    assert clean_text("  hello   world  ") == "hello world"
    assert clean_text(None) == ""


def test_detect_nism_required():
    assert detect_nism_required("NISM Series V-A required") is True
    assert detect_nism_required("Python developer role") is False


def test_compute_relevance_score_high():
    record = {
        "position": "NISM Mutual Fund Advisor",
        "job_description": "NISM certification mandatory",
        "nism_required": True,
        "posted_date": str(__import__('datetime').date.today()),
    }
    score = compute_relevance_score(record)
    assert score >= 80


def test_transform_skips_empty():
    records = [{"company_name": "", "position": ""}]
    result = transform(records)
    assert len(result) == 0


def test_transform_full():
    records = [{
        "company_name": "TestCo", "position": "NISM Analyst",
        "salary": "5L", "location": "Mumbai", "source": "LinkedIn",
    }]
    result = transform(records)
    assert len(result) == 1
    assert "relevance_score" in result[0]
