import json, os, sys, tempfile
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from etl.extractor import extract_from_json, extract_from_csv


def test_extract_from_json():
    sample = [{"company_name": "TestCo", "position": "Analyst", "source": "Manual"}]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(sample, f)
        path = f.name
    result = extract_from_json(path)
    assert len(result) == 1
    assert result[0]["company_name"] == "TestCo"
    os.unlink(path)


def test_extract_returns_list():
    sample = [{"company_name": "Co", "position": "Dev"}]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(sample, f)
        path = f.name
    result = extract_from_json(path)
    assert isinstance(result, list)
    os.unlink(path)
