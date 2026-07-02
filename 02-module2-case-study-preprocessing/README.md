# 2. Module 2 Case Study — End-to-End Preprocessing on a Real Dataset

**Module:** 2 (Day 11) · **Type:** Case Study

## Objective
Take a messier, multi-source dataset through the full preprocessing pipeline:
cleaning, feature engineering, integration, feature selection, dimensionality
reduction.

## Prerequisite skills (from this module)
Handling missing values/outliers, encoding & scaling, SQL queries/joins, merging
multiple sources, correlation-based feature selection, PCA.

## Dataset
Something that legitimately needs cleaning and comes in more than one piece, e.g.:
- Kaggle "House Prices" or "Loan Prediction" (missing values + categorical encoding)
- Two related CSVs you join yourself (e.g. a transactions table + a customers table) to exercise the SQL/merge step
- Load at least one piece via SQL (SQLite is fine: `sqlite3` + `pandas.read_sql`)

## Tasks
1. Load raw data from 2+ sources; merge/join them into one working table.
2. Clean: impute or drop missing values, treat outliers (document the rule you used).
3. Encode categoricals (one-hot / label encoding as appropriate) and scale numerics.
4. Run correlation analysis and pick a reduced feature set; justify what you dropped.
5. Apply PCA and compare explained variance for 2–3 component counts.
6. Wrap steps 2–5 into a single reusable function/pipeline (`src/pipeline.py`), not just notebook cells.

## Deliverable
- `notebooks/case_study.ipynb` — walkthrough with reasoning at each step
- `src/pipeline.py` — the reusable preprocessing pipeline (callable on new raw data)
- `data/raw/` and `data/processed/` — before/after datasets

## Done when
Running `src/pipeline.py` against the raw data reproduces the processed dataset,
and you can explain why each cleaning/encoding choice was made.
