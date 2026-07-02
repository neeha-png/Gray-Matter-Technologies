# Self-Mock Evaluation — Readiness Against Modules 1–6

Honest checklist: what's actually been demonstrated with working code and
real results across the 10 projects, versus what's still outstanding before
the final assessment. Checked items link to the project that proves it, not
just a topic that was read about.

## Module 1 — Foundations of Programming & Mathematics for AI
- [x] Python basics, control flow, functions, data structures — project 1
- [x] NumPy, Pandas — project 1
- [x] Data visualization (Matplotlib/Seaborn) — project 1
- [x] Linear algebra, statistics, probability — project 1 (conditional
      probability of survival by class/sex on the Titanic dataset)

## Module 2 — Data Preprocessing & EDA
- [x] Cleaning, missing values, outliers — project 2 (documented, justified rules)
- [x] Feature engineering: encoding, scaling — project 2
- [x] SQL queries/joins — project 2 (real SQLite join between two tables)
- [x] Feature selection (correlation-based), PCA — project 2
- [x] Advanced visualization (heatmaps, pairplots), storytelling — project 3

## Module 3 — Machine Learning Fundamentals
- [x] Regression, classification, KNN, decision trees, random forest — project 4
- [x] Model evaluation (accuracy/precision/recall/F1) — project 4
- [x] Cross-validation vs. single split — project 4
- [x] Overfitting/underfitting diagnosis — project 4 (real diagnosed
      overfitting: 96% train vs. 72% test accuracy on default Random Forest)
- [x] Hyperparameter tuning (GridSearchCV) — project 4
- [x] Deployed prediction system (Streamlit) — project 5, verified working
      in a live browser test

## Module 4 — Advanced ML & Deep Learning
- [x] Neural network basics, CNNs — project 6
- [x] Dropout, batch normalization — project 6 (measured effect, not just applied)
- [x] Transfer learning — project 6 (ResNet18, ImageNet weights)
- [ ] **Framework gap:** curriculum names TensorFlow/Keras; this machine's
      Python version (3.14) has no TensorFlow build, so **PyTorch was used
      instead** (documented, with reasoning). Conceptually equivalent, but
      Keras-specific syntax hasn't been hands-on practiced.
- [ ] **RNN/LSTM (sequence track) not practiced.** Project 6 deliberately
      picked the image track per the "pick ONE track" instruction — worth a
      quick RNN/LSTM refresher before an assessment that might test it.
- [x] GPU training — not available on this machine; explicitly reported
      (no GPU present), not faked. Concept understood, not hands-on run.
- [x] Deployed image-classification app with documented failure cases — project 7

## Module 5 — NLP, Computer Vision & Real-Time Applications
- [x] Text processing, TF-IDF — project 8
- [x] Sentiment analysis — project 8 (real F1 score: 0.817 on 2,748 real reviews)
- [ ] **Transformers/attention mechanism — conceptual only, not hands-on.**
      Project 8 used TF-IDF + Logistic Regression (deliberately, for speed
      and to avoid another framework-compatibility risk), not a transformer
      model. Worth practicing a HuggingFace transformer fine-tune separately.
- [ ] **Computer vision object detection, recommendation systems, time-series
      forecasting — not covered.** The "pick ONE scenario" instruction in
      project 8 was followed (NLP), so these three alternate tracks were
      not hands-on practiced. Same caveat as Module 4's single-track choice.
- [x] REST API integration — project 8 (real Flask API, tested end-to-end
      with a live client script)
- [x] Real-time ML app — project 9, verified in a live browser including
      the API-down error state

## Module 6 — MLOps, Deployment & Latest Trends
- [x] Model deployment (Flask/Streamlit) — projects 5, 8, 9
- [x] **Docker — built and run locally, exactly as the brief asks.**
      Installing Docker Desktop first required enabling WSL2 (needed
      `wsl --install` from an elevated PowerShell plus a restart — a real,
      not assumed, Windows prerequisite). Once running: `docker build`
      succeeded, `docker run` started the container on port 5001, and
      `/health`, `/predict`, and `/explain` were all hit for real against
      the running container (not the local Flask dev server) — `/explain`
      returned a genuine Groq-generated explanation. Container logs
      confirmed clean gunicorn startup with 2 workers and no errors.
- [x] CI/CD — `.github/workflows/ci.yml` written and YAML-validated
      (lint + test + Docker build/smoke-test on push, nightly ETL cron).
- [x] Version control — **done.** `git init` in place, 12+ commits pushed to
      `https://github.com/neeha-png/Gray-Matter-Technologies` (branch
      `main`), verified in sync with `git fetch` + `git log origin/main`.
- [ ] **Cloud deployment — partially live; container blocked on a real
      billing decision, not a technical one.** `wrangler deploy` was run for
      real: the Worker script, static front-end, and bindings all deployed
      successfully to Cloudflare. The container push failed with a genuine
      `401 Unauthorized` from Cloudflare's container registry — traced this
      to **Cloudflare Containers requiring the Workers Paid plan
      ($5/month, no free tier)**, confirmed via current docs/web search,
      not assumed. Asked the user whether to upgrade; they chose to hold
      off for now. So today: the static page + Worker routing are live on
      Cloudflare; the container/API itself is not, purely because it
      would cost real money and the user opted not to spend it yet. Local
      container dev via `wrangler dev` still needs WSL for its container
      simulation specifically (separate from the WSL now installed for
      Docker Desktop) — confirmed via `wrangler dev`'s own error message.
- [x] Monitoring — `monitoring/check_health.py`, tested against real
      logged predictions; correctly flagged a real sentiment-drift alert
      (50% vs. 68.7% training baseline) in a live test
- [x] Data engineering / ETL — `etl/refresh_reviews.py`, tested twice
      (first run: 2,748 new reviews found; second run: correctly found 0 new)
- [x] **GenAI add-on — live-tested end-to-end, working.** Gemini was tried
      first: the key authenticated correctly, but the Google Cloud project
      behind it had a hard **zero quota** for `gemini-2.0-flash` on the free
      tier and required enabling billing to get any quota at all. Also
      found and fixed a real bug during that test: the key was being logged
      in plain text whenever the call failed (passed as a `?key=` query
      param; `requests`' exception messages embed the full URL) — fixed by
      switching to a header instead. Rather than ask for a card, **switched
      `/explain` to Groq** (`api.groq.com`, OpenAI-compatible chat
      completions, model `llama-3.3-70b-versatile`, confirmed free/no-card
      via current docs). With a real `GROQ_API_KEY` supplied, ran the app
      live in a browser end-to-end: a negative review correctly got
      "The review was likely classified as 'negative' because it mentions
      the product broke quickly and the customer had a bad experience with
      the company's support," and a positive review got a matching
      real explanation — both `/explain` calls returned `200`, confirmed
      in the server logs with no key ever appearing in them. The key is
      also uploaded as a real Cloudflare secret, ready for deployment.
- [x] Architecture write-up — `ARCHITECTURE.md`

## Bottom line

Everything that can be verified **without ongoing real money being spent**
has now been built and actually tested — the ML pipeline, the API, the
monitoring, the ETL, the CI config, Git/GitHub, Docker (built and run for
real, locally), and the GenAI add-on (real Groq explanations, live).
`wrangler deploy` was run for real too: the Worker and static front-end are
genuinely live on Cloudflare. The one thing left open — deploying the
container itself — turned out to need Cloudflare's $5/month Workers Paid
plan (no free tier exists for Containers); the user was asked and chose
not to spend that yet, so it's a deliberate, informed pause, not a gap in
what's been built or tested. The "framework substitution" and
"single-track" notes from Modules 4–5 are unchanged and are the most
likely genuine assessment risk — worth a quick review of Keras syntax and
transformers/CV/RecSys/time-series basics before test day.
