"""Production version of the sentiment API from project 8, extended for the
capstone with:
- structured request/prediction logging (for monitoring)
- a GenAI /explain endpoint (Groq) that turns a raw prediction into a
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

# Groq's free tier needs no credit card (unlike Gemini, which required
# billing to be enabled for this account) and speaks the same
# OpenAI-compatible chat completions format most providers use.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

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


@app.get("/")
def index():
    # In production the Worker serves src/static/ directly and only routes
    # /health, /predict, /explain here. Locally, serving it from Flask too
    # lets the page and the API share one origin so you can check the whole
    # thing in a browser without Docker/Cloudflare.
    return app.send_static_file("index.html")


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
    English explanation, using Groq. Requires GROQ_API_KEY to be set."""
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY is not configured on this server"}), 503

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
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100,
            },
            timeout=10,
        )
        response.raise_for_status()
        body = response.json()
        explanation = body["choices"][0]["message"]["content"].strip()
    except Exception as e:
        # Log only the status/reason, never the exception's str() -- avoids
        # ever writing the Authorization header or key into this log file.
        status = getattr(getattr(e, "response", None), "status_code", "n/a")
        logger.error(f"Groq explain call failed: status={status} ({type(e).__name__})")
        return jsonify({"error": "Could not generate an explanation right now"}), 502

    return jsonify({"text": text, "sentiment": sentiment, "explanation": explanation})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
