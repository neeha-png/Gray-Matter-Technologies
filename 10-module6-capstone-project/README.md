# 10. Module 6 Capstone Project — End-to-End Industry Solution

**Module:** 6 (Day 11) · **Type:** Capstone (feeds into Day 12 Final Review / Self-Mock evaluation)

## Objective
Take one of the earlier projects (recommended: project 9's AI product, or
project 5's prediction system) and productionize it end-to-end using
everything in Module 6: version control, containerization, CI/CD, cloud
deployment, monitoring, and a GenAI add-on.

## Prerequisite skills
Git/GitHub, Flask/Streamlit deployment, Docker, CI/CD pipelines, AWS/GCP
basics, model monitoring, ETL basics, LLMs/chatbots, prompt engineering.

## Tasks
1. **Version control:** put the chosen project in a Git repo with a clean
   commit history and a `.gitignore` (exclude large model/data files).
2. **Containerize:** write a `Dockerfile` for the app; build and run it locally.
3. **CI/CD:** set up a basic pipeline (GitHub Actions is simplest) that runs
   tests/lint on push and builds the Docker image.
4. **Cloud deployment:** deploy the container to a free/low-cost tier on
   AWS or GCP (e.g. AWS App Runner/ECS, or GCP Cloud Run).
5. **Monitoring:** add basic logging of predictions/requests and a simple
   dashboard or log-based check for model drift or errors.
6. **Data engineering:** if the app has an ongoing data feed, add a minimal
   ETL step (scheduled script or cloud function) that refreshes input data.
7. **GenAI add-on:** integrate an LLM-based feature relevant to the product
   (e.g. a chatbot that explains predictions, or auto-generated summaries of
   results) using prompt engineering techniques from Day 10.
8. **Final review prep:** write up the full architecture (1-pager) and run a
   self-mock evaluation against the program's stated learning outcomes.

## Deliverable
- A GitHub repo containing: app code, `Dockerfile`, CI/CD config (`.github/workflows/`), deployment notes
- A live (or reproducible-on-demand) cloud deployment URL
- `ARCHITECTURE.md` — 1-page write-up of the full system
- `SELF_MOCK_EVALUATION.md` — your own assessment-readiness checklist against Modules 1–6

## Done when
Someone else could clone the repo, read `ARCHITECTURE.md`, and understand how
data flows from input through model to the deployed, monitored product —
and the assessment prep checklist is fully checked off.
