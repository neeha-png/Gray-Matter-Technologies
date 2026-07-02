"""Reads the prediction log the API writes (monitoring/logs/predictions.jsonl)
and reports whether anything looks off -- a lightweight, log-based
alternative to a full monitoring dashboard.

Run it any time:
    python monitoring/check_health.py
"""
import json
import pathlib
import statistics
import sys

LOG_PATH = pathlib.Path(__file__).resolve().parent / "logs" / "predictions.jsonl"

# Baselines from the training data (project 8): about 69% of labeled reviews
# were positive. If live traffic's sentiment mix drifts far from that, it's
# worth a human looking at *why* -- new product line, review-bombing, etc.
BASELINE_POSITIVE_RATE = 0.687
DRIFT_THRESHOLD = 0.15          # flag if live positive-rate differs by more than this
LOW_CONFIDENCE_THRESHOLD = 0.65  # matches the app's own "uncertain" cutoff
LOW_CONFIDENCE_RATE_ALERT = 0.30 # flag if >30% of predictions are low-confidence


def load_records():
    if not LOG_PATH.exists():
        return []
    with open(LOG_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    records = load_records()
    if not records:
        print(f"No predictions logged yet at {LOG_PATH}. Nothing to check.")
        return

    n = len(records)
    positive_rate = sum(1 for r in records if r["sentiment"] == "positive") / n
    avg_confidence = statistics.mean(r["confidence"] for r in records)
    low_confidence_rate = sum(1 for r in records if r["confidence"] < LOW_CONFIDENCE_THRESHOLD) / n
    avg_latency = statistics.mean(r["latency_ms"] for r in records)

    print(f"Checked {n} logged predictions from {LOG_PATH}")
    print(f"  Positive rate:        {positive_rate:.1%}  (training baseline: {BASELINE_POSITIVE_RATE:.1%})")
    print(f"  Average confidence:   {avg_confidence:.2f}")
    print(f"  Low-confidence rate:  {low_confidence_rate:.1%}  (< {LOW_CONFIDENCE_THRESHOLD})")
    print(f"  Average latency:      {avg_latency:.1f} ms")

    alerts = []
    if abs(positive_rate - BASELINE_POSITIVE_RATE) > DRIFT_THRESHOLD:
        alerts.append(
            f"Sentiment mix has drifted: live positive-rate is {positive_rate:.1%}, "
            f"vs. a {BASELINE_POSITIVE_RATE:.1%} training baseline. "
            "Worth checking whether the kind of reviews coming in has changed."
        )
    if low_confidence_rate > LOW_CONFIDENCE_RATE_ALERT:
        alerts.append(
            f"{low_confidence_rate:.1%} of predictions are low-confidence (<{LOW_CONFIDENCE_THRESHOLD}) -- "
            "higher than expected. The model may be seeing text unlike its training data."
        )

    print()
    if alerts:
        print("ALERTS:")
        for a in alerts:
            print(f"  - {a}")
        sys.exit(1)
    else:
        print("No alerts -- traffic looks consistent with training-time expectations.")


if __name__ == "__main__":
    main()
