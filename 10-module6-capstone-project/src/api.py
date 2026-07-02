"""Production version of the sentiment API from project 8, extended for the
capstone with:
- structured request/prediction logging (for monitoring)
- a GenAI /explain endpoint (Gemini) that turns a raw prediction into a
  plain-English explanation

Run it:
    python src/api.py
Reachable at http://localhost:5000
"""
import json
import logging
import os
import pathlib
import time

import joblib
import requests
from flask import Flask, jsonify, request

MODEL_PATH = pathlib.Path(__file__).resolve().parent / "sentiment_model.pkl"
LOG_DIR = pathlib.Path(__file__).resolve().parent.parent / "monitoring" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
PREDICTIONS_LOG = LOG_DIR / "predictions.jsonl"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)

app = Flask(__name__)
model = joblib.load(MODEL_PATH)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentiment-api")


def log_prediction(text: str, sentiment: str, confidence: float, latency_ms: float):
    """Append one structured record per prediction -- this is what the
    monitoring/check_health.py script reads to look for drift/errors."""
    record = {
        "timestamp": time.time(),
        "text_length": len(text),
        "sentiment": sentiment,
        "confidence": confidence,
        "latency_ms": round(latency_ms, 1),
    }
    with open(PREDICTIONS_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")


@app.after_request
def add_cors_headers(response):
    # The front-end is served from a different origin (Cloudflare), so it
    # needs explicit CORS permission to call this API.
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/predict")
def predict():
    start = time.time()
    data = request.get_json(silent=True) or {}
    text = data.get("text")

    if not text or not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Request body must include a non-empty 'text' field"}), 400

    prediction = model.predict([text])[0]
    confidence = float(model.predict_proba([text])[0].max())
    sentiment = "positive" if prediction == 1 else "negative"

    latency_ms = (time.time() - start) * 1000
    log_prediction(text, sentiment, confidence, latency_ms)
    logger.info(f"predict sentiment={sentiment} confidence={confidence:.2f} latency={latency_ms:.1f}ms")

    return jsonify({
        "text": text,
        "sentiment": sentiment,
        "confidence": round(confidence, 3),
    })


@app.post("/explain")
def explain():
    """GenAI add-on: turn the raw prediction into a one-sentence plain
    English explanation, using Gemini. Requires GEMINI_API_KEY to be set."""
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY is not configured on this server"}), 503

    data = request.get_json(silent=True) or {}
    text = data.get("text")
    sentiment = data.get("sentiment")
    confidence = data.get("confidence")

    if not text or not sentiment:
        return jsonify({"error": "Request body must include 'text' and 'sentiment'"}), 400

    prompt = (
        "You are helping a customer support agent understand an automated "
        "sentiment prediction. In ONE short, plain-English sentence (no "
        "jargon), explain why this review was likely classified as "
        f"'{sentiment}' (confidence {confidence}). "
        f"Review: \"{text}\""
    )

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=10,
        )
        response.raise_for_status()
        body = response.json()
        explanation = body["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        logger.error(f"Gemini explain call failed: {e}")
        return jsonify({"error": "Could not generate an explanation right now"}), 502

    return jsonify({"text": text, "sentiment": sentiment, "explanation": explanation})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
