"""REST API serving the customer-review sentiment model trained in the
case study notebook.

Run it:
    python src/api.py
Then it's reachable at http://localhost:5000

Endpoints:
    GET  /health           -> {"status": "ok"}
    POST /predict          -> body {"text": "..."} -> sentiment + confidence
"""
import pathlib

import joblib
from flask import Flask, jsonify, request

MODEL_PATH = pathlib.Path(__file__).resolve().parent.parent / "sentiment_model.pkl"

app = Flask(__name__)
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text")

    if not text or not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Request body must include a non-empty 'text' field"}), 400

    prediction = model.predict([text])[0]
    confidence = model.predict_proba([text])[0].max()

    return jsonify({
        "text": text,
        "sentiment": "positive" if prediction == 1 else "negative",
        "confidence": round(float(confidence), 3),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
