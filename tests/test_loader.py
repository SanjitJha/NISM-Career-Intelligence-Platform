"""
Loader tests — uses a mock to avoid real DB calls during CI.
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def test_load_jobs_returns_dict(monkeypatch):
    """load_jobs should return a dict with 'inserted' and 'skipped' keys."""
    from etl import loader
    monkeypatch.setattr(loader, "execute_query", lambda *a, **k: None)
    result = loader.load_jobs([{
        "company_name": "X", "position": "Y", "salary": "5L",
        "location": "Mumbai", "experience_required": "1y",
        "nism_required": True, "source": "LinkedIn",
        "apply_link": "", "job_description": "", "relevance_score": 80,
        "posted_date": "2024-01-01",
    }])
    assert "inserted" in result
    assert "skipped" in result
