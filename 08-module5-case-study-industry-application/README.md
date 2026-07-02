# 8. Module 5 Case Study — Industry Application

**Module:** 5 (Day 11) · **Type:** Case Study

## Objective
Solve one realistic industry-style problem by combining the Module 5 topics —
NLP, computer vision, recommendation systems, or time-series forecasting —
with an API integration, rather than just modeling in isolation.

## Prerequisite skills
Text processing/TF-IDF, sentiment analysis, transformer basics, OpenCV/object
detection basics, collaborative filtering, time-series forecasting, REST APIs.

## Pick ONE realistic scenario
- **NLP:** sentiment analysis on customer reviews, surfaced through a small API
- **CV:** object detection on a product/inventory image set
- **RecSys:** a movie/product recommender using collaborative filtering
- **Time series:** demand or sales forecasting for a retail-style dataset

## Tasks
1. Frame the business problem in 2–3 sentences (who needs this, what decision it informs).
2. Build the model (sentiment classifier / object detector / recommender / forecaster).
3. Evaluate with the metric that matters for the scenario (F1 for sentiment,
   mAP/IoU for detection, precision@k for recsys, MAE/RMSE for forecasting).
4. Expose the model behind a REST endpoint (Flask/FastAPI) — this is the
   "APIs Integration" requirement from Day 9 of this module.
5. Call the API from a small client script or notebook to prove it works end-to-end.

## Deliverable
- `notebooks/case_study.ipynb` — modeling + evaluation
- `src/api.py` — the REST API serving the model
- `src/client_test.py` — a script hitting the API and printing results

## Done when
`src/api.py` runs, and `src/client_test.py` gets back a correct-shaped response
for at least 3 test inputs.
