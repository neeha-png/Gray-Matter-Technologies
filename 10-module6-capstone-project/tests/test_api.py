"""Smoke tests for the sentiment API, run in CI on every push (see
.github/workflows/ci.yml). Uses Flask's test client, so no server needs to
actually be running.
"""
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / "src"))

import api  # noqa: E402


def get_client():
    api.app.testing = True
    return api.app.test_client()


def test_health():
    client = get_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_predict_positive_review():
    client = get_client()
    response = client.post("/predict", json={"text": "This is absolutely fantastic, I love it!"})
    assert response.status_code == 200
    body = response.get_json()
    assert body["sentiment"] == "positive"
    assert 0.0 <= body["confidence"] <= 1.0


def test_predict_negative_review():
    client = get_client()
    response = client.post("/predict", json={"text": "Terrible product, completely broken on arrival."})
    assert response.status_code == 200
    body = response.get_json()
    assert body["sentiment"] == "negative"
    assert 0.0 <= body["confidence"] <= 1.0


def test_predict_rejects_empty_text():
    client = get_client()
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_predict_rejects_missing_text_field():
    client = get_client()
    response = client.post("/predict", json={})
    assert response.status_code == 400


def test_explain_without_api_key_returns_503():
    client = get_client()
    # In CI there's no GEMINI_API_KEY configured -- the endpoint should fail
    # gracefully (503), not crash.
    response = client.post("/explain", json={"text": "ok", "sentiment": "positive", "confidence": 0.9})
    assert response.status_code in (503, 200)  # 200 only if a real key happens to be set
