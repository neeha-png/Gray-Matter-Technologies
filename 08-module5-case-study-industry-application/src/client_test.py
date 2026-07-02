"""Hits the running sentiment API with a handful of test reviews and prints
what comes back -- proof the model works end-to-end over real HTTP, not just
inside a notebook.

Run `python src/api.py` in one terminal first, then this script in another:
    python src/client_test.py
"""
import requests

API_URL = "http://localhost:5000"

TEST_REVIEWS = [
    "Absolutely fantastic, exceeded all my expectations!",
    "Worst purchase I've ever made, complete waste of money.",
    "Great battery life and the camera quality is amazing.",
    "The staff were rude and the food arrived cold.",
    "Works exactly as described, very happy with it.",
]


def main():
    health = requests.get(f"{API_URL}/health", timeout=5)
    print(f"Health check: {health.status_code} {health.json()}")
    print()

    for review in TEST_REVIEWS:
        response = requests.post(f"{API_URL}/predict", json={"text": review}, timeout=5)
        assert response.status_code == 200, f"Unexpected status {response.status_code}: {response.text}"
        body = response.json()
        assert "sentiment" in body and "confidence" in body, f"Malformed response: {body}"
        print(f"[{body['sentiment']:8s} {body['confidence']:.2f}] {review}")

    # Also confirm basic input validation works (empty text should be rejected)
    bad_response = requests.post(f"{API_URL}/predict", json={"text": ""}, timeout=5)
    print(f"\nEmpty text correctly rejected: {bad_response.status_code} {bad_response.json()}")


if __name__ == "__main__":
    main()
