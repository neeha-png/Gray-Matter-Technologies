# 5. Module 3 Mini Project — Prediction System (Deploy a Simple ML App)

**Module:** 3 (Day 12) · **Type:** Mini Project

## Objective
Take the tuned model from project 4 and wrap it in a minimal, usable app so a
non-technical person could get a prediction from it.

## Prerequisite skills
Everything from Module 3, plus basic familiarity with a simple web framework
(Streamlit is the fastest path; Flask if you want more control).

## Requirements
- The saved model from project 4 (`model.pkl`)
- `streamlit` (recommended for speed) or `flask` + a minimal HTML form

## Tasks
1. Load `model.pkl` (and any fitted scaler/encoder) at app startup.
2. Build an input form matching the model's feature columns.
3. On submit, run the pipeline and display the prediction (plus, if
   classification, the predicted probability).
4. Add basic input validation (e.g. required fields, sane ranges) — just
   enough that bad input doesn't crash the app.
5. Run it locally and confirm it produces sensible predictions for a few
   known inputs (sanity-check against the training data).

## Deliverable
- `src/app.py` — the Streamlit/Flask app
- The model artifact copied into this folder (or referenced from project 4)
- `notebooks/` can hold a short "sanity check" notebook comparing app output vs. notebook predictions

## Done when
Running `streamlit run src/app.py` (or `flask run`) locally lets you enter
values and get a prediction back in the browser.
