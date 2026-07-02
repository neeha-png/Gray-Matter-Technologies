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
- [ ] **Docker — written, config-validated, still not locally `docker
      build`-verified.** `Dockerfile` is correct per `wrangler`'s config/type
      checks (bindings/container resolved correctly), but Docker isn't
      installed on this machine, so the image itself has never actually been
      built end-to-end here. Will be built and smoke-tested for real by CI
      on push (GitHub's Ubuntu runners ship Docker).
- [x] CI/CD — `.github/workflows/ci.yml` written and YAML-validated
      (lint + test + Docker build/smoke-test on push, nightly ETL cron);
      **not yet run for real** — today's changes (Gemini wiring, the log
      security fix) haven't been pushed yet, so CI hasn't executed against
      this repo at all so far.
- [x] Version control — **done.** `git init` in place, 11 project commits
      plus a merge commit, pushed to
      `https://github.com/neeha-png/Gray-Matter-Technologies` (branch
      `main`), verified in sync with `git fetch` + `git log origin/main`.
- [ ] **Cloud deployment — logged in and wired up, still not live.**
      `wrangler whoami` confirms an authenticated Cloudflare account
      (neehasm0@gmail.com) with the right token scopes (`containers`,
      `workers`, etc.). The `GEMINI_API_KEY` secret has been uploaded to
      Cloudflare via `wrangler secret put`, and the container class now
      forwards it from the Worker's env into the Flask container's process
      env (`envVars`), typechecked clean. **`wrangler deploy` itself has
      deliberately not been run** — it's a live, billable action, and the
      user asked to verify everything locally first. Local container dev
      still needs WSL (Windows limitation, confirmed directly via `wrangler
      dev`'s own error message, not assumed).
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

Everything that could be verified **without a live/billable cloud action**
has now been built and actually tested — the ML pipeline, the API, the
monitoring, the ETL, the CI config, the Docker/Worker config, Git/GitHub,
and Cloudflare login. Only one thing remains genuinely open, and it's by
choice, not inability: `wrangler deploy` itself — ready to run,
intentionally held back pending the user's go-ahead since it's a live,
billable action. Everything else, including the GenAI add-on, is now
live-tested end-to-end with real credentials. Docker remains locally
unverified (no Docker on this
machine) but is expected to build cleanly in CI. The "framework
substitution" and "single-track" notes from Modules 4–5 are unchanged and
are the most likely genuine assessment risk — worth a quick review of
Keras syntax and transformers/CV/RecSys/time-series basics before test day.
