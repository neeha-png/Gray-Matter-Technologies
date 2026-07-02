# Gray Matter Technologies — Deep Skilling Stream 1 (AI/ML) — Project Plan

> New here? Read **[START_HERE.md](START_HERE.md)** first for a plain-language,
> no-jargon walkthrough of what each project actually is.

Source: `GrayMatter_AIML_DeepSkilling ToC.pdf`. This folder holds the 10 practical
deliverables (mini-projects, case studies, capstone) called for across the 6 modules
of the 3-month program, in the order they should be attempted.

Each project has its own numbered subfolder with a `README.md` (objective, required
skills/tools, dataset guidance, task breakdown, deliverable) and starter `data/`,
`notebooks/`, `src/` folders.

## Why this order
The sequence follows the program's module order exactly, because each project
depends on skills only introduced up to that point (e.g. you can't do the ML
pipeline case study before regression/classification/evaluation are covered in
Module 3). Don't skip ahead — later projects reuse earlier ones (the Module 3
prediction system reuses the Module 2 cleaned dataset; the capstone reuses/extends
the Module 5 AI product).

## Project sequence

| # | Folder | Module | Type | What you build |
|---|--------|--------|------|-----------------|
| 1 | `01-module1-mini-project-eda` | 1 (Day 12) | Mini Project | EDA on a real dataset using Python/NumPy/Pandas/stats |
| 2 | `02-module2-case-study-preprocessing` | 2 (Day 11) | Case Study | End-to-end cleaning, feature engineering, SQL merge, PCA |
| 3 | `03-module2-mini-project-eda-insights` | 2 (Day 12) | Mini Project | Advanced EDA + insights presentation |
| 4 | `04-module3-case-study-ml-pipeline` | 3 (Day 11) | Case Study | End-to-end supervised ML pipeline with tuning |
| 5 | `05-module3-mini-project-prediction-system` | 3 (Day 12) | Mini Project | Deploy a simple ML prediction app |
| 6 | `06-module4-case-study-deep-learning-app` | 4 (Day 10) | Case Study | Real deep learning project (CNN/RNN/LSTM/Transfer Learning) |
| 7 | `07-module4-mini-project-image-text-ai` | 4 (Day 11) | Mini Project | Image or text AI application |
| 8 | `08-module5-case-study-industry-application` | 5 (Day 11) | Case Study | Solve a real industry problem (NLP/CV/RecSys/time series) |
| 9 | `09-module5-mini-project-ai-product` | 5 (Day 12) | Mini Project | End-to-end AI product with API integration |
| 10 | `10-module6-capstone-project` | 6 (Day 11) | Capstone | Full MLOps deployment: Docker, CI/CD, cloud, monitoring, GenAI |

## Suggested cadence
Each project maps to the "Case Study"/"Mini Project" day(s) in its module, but
budget 2–4 extra evenings per project beyond the single listed day if you're
self-teaching the underlying topic for the first time. Don't move to the next
numbered folder until the current one's deliverable (checked off in its README)
is done — the Day 12 "Final Review / Self-Mock evaluation" in Module 6 assumes
all 10 are complete and working.

## Common setup (once)
- Python 3.10+, `venv` or `conda`
- Core libs: `numpy pandas matplotlib seaborn scikit-learn jupyter`
- Module 4+: `tensorflow` (or `torch`), `opencv-python`
- Module 6: `flask` or `streamlit`, `docker`, a free-tier AWS/GCP account, `git`
- A GitHub account/repo per project (or one repo with these folders) for Module 6's version-control requirement
