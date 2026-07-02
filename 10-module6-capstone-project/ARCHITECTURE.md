# Architecture — Review Triage Assistant (Capstone)

Productionized version of project 9's AI product: a sentiment-analysis
service (from project 8) with a static front end, deployed on Cloudflare,
monitored, and extended with an LLM-based explanation feature.

## Data flow, end to end

```
Browser
  │  GET /            (loads the page)
  │  POST /predict     POST /explain
  ▼
Cloudflare Worker  (worker/src/index.ts)
  │  - Static routes  -> served from src/static/ (Workers Static Assets, GA)
  │  - /health,/predict,/explain -> routed to the container (Containers, beta)
  ▼
Cloudflare Container  (Dockerfile, running src/api.py via gunicorn)
  │  - Loads sentiment_model.pkl (TF-IDF + Logistic Regression, from project 8)
  │  - /predict: text -> {sentiment, confidence}
  │  - /explain: prediction -> calls Groq API -> plain-English explanation
  │  - Every /predict call is logged to monitoring/logs/predictions.jsonl
  ▼
Groq API (external, GenAI add-on)            Monitoring / ETL (offline)
  - one-sentence explanation of              - monitoring/check_health.py reads
    why a review was classified that way       the prediction log, flags drift
                                                (sentiment mix vs. training
                                                baseline) or excess low-confidence
                                                predictions
                                              - etl/refresh_reviews.py pulls new
                                                review data on a schedule (nightly
                                                GitHub Actions cron), dedupes by
                                                content hash, lands new batches in
                                                data/incoming/ for future retraining
```

## Why this shape

- **Static assets on Workers, not Streamlit.** Cloudflare has no GA product
  for long-running Python/Streamlit processes. Workers Static Assets is GA,
  free, and instant — the same UI (paste a review, get a verdict) works
  fine as a small HTML/JS page calling the API via `fetch`.
- **Flask API on Cloudflare Containers (beta).** Containers can run an
  arbitrary Docker image, which is what the existing scikit-learn/joblib
  model needs. It's explicitly beta (no SLA, rolling deploys, manual load
  balancing via `getRandom`) — a real, documented trade-off, not hidden.
- **GenAI add-on calls Groq directly from the container**, not from the
  Worker — keeps the API key and prompt logic in one place (`src/api.py`),
  and the Worker stays a thin router. Groq was chosen over Gemini because
  its free tier needs no credit card; Gemini required enabling billing on
  this account even to stay within its free-tier limits.

## CI/CD (`.github/workflows/ci.yml`)

- **On every push/PR:** install deps, lint (`ruff`), run `tests/test_api.py`
  (Flask test-client smoke tests — no live server needed), then build the
  Docker image on the runner and smoke-test it with a real `/health` call.
- **Nightly (cron):** runs `etl/refresh_reviews.py` to demonstrate the
  scheduled-refresh pattern.

## Known limitations (stated plainly, not hidden)

- **Cloudflare Containers is in beta.** API can change; no SLA.
- **Local container dev doesn't work natively on Windows** — confirmed
  directly (`wrangler dev` errors with "Local development with containers is
  currently not supported on Windows. You should use WSL instead."). The
  config itself validated correctly (bindings resolved, container detected);
  only the local Windows dev loop is blocked. WSL, macOS, or Linux CI runners
  are unaffected.
- **Docker was installed, and the image was built and run for real**
  (required enabling WSL2 first via `wsl --install`, then a restart).
  `/health`, `/predict`, and `/explain` were all verified against the
  running container directly, not just the local Flask dev server.
- **Cloudflare Containers requires the $5/month Workers Paid plan** —
  there's no free tier for Containers specifically (confirmed via current
  Cloudflare docs). `wrangler deploy` was run for real: the Worker script
  and static front-end deployed successfully and are genuinely live; the
  container push failed with a real `401 Unauthorized` from Cloudflare's
  registry until that plan is active. The user was asked and chose to hold
  off on the $5/month upgrade for now, so the API/container is built,
  tested, and ready, but not currently live on the public internet.
- **The ETL step operates on a static public dataset**, standing in for a
  real live review feed — the refresh/dedupe *pattern* is real and tested
  (verified: second run correctly finds 0 new reviews), the *data source*
  is a stand-in.
