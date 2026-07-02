# 9. Module 5 Mini Project — AI Product (End-to-End App)

**Module:** 5 (Day 12) · **Type:** Mini Project

## Objective
Turn project 8's API-backed model into a real "product": a live app a user
can interact with, closing the loop from Day 10's "Real-Time ML Apps" topic.

## Prerequisite skills
Everything from project 8, plus building a simple interactive front end
around a live API.

## Requirements
- The API from project 8 (`08-module5-case-study-industry-application/src/api.py`)
- `streamlit` (fastest) or a lightweight HTML/JS front end calling the API via `fetch`/`requests`

## Tasks
1. Stand up the project 8 API locally (or reuse it directly if kept running).
2. Build a front end: user provides input (review text / image / user id / date
   range depending on your Module 5 scenario), app calls the API, and displays
   results in real time.
3. Add a loading/error state (what happens if the API is down or input is invalid).
4. Record a short before/after: what the raw model output looks like vs. what
   the polished product shows the user.
5. Write a 1-paragraph "product pitch": who is this for, what problem does it solve.

## Deliverable
- `src/app.py` — the end-user-facing app
- `PRODUCT_PITCH.md` — the short pitch
- Screenshot(s) of the running app in `notebooks/` or the project root

## Done when
A person with no ML background could open the app, use it, and understand the
result without you explaining the model underneath.
