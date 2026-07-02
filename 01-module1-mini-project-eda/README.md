# 1. Module 1 Mini Project — Exploratory Data Analysis on a Real Dataset

**Module:** 1 (Day 12) · **Type:** Mini Project

## Objective
Apply everything from Module 1 — Python basics, NumPy, Pandas, visualization,
linear algebra, statistics, probability — to explore a single real dataset end
to end and produce written insights.

## Prerequisite skills (from this module)
Python control flow/functions, NumPy arrays, Pandas DataFrames, Matplotlib/Seaborn,
mean/median/variance, basic probability.

## Dataset
Pick one small, clean, well-known dataset so the focus stays on technique, not
data-wrangling pain:
- Titanic (Kaggle) — classification-flavored, mixed types, some missing values
- Iris or Palmer Penguins — simple numeric, good for stats/plots
- Any single CSV from Kaggle/UCI you're personally interested in

## Tasks
1. Load the dataset into a Pandas DataFrame; inspect shape, dtypes, `.info()`, `.describe()`.
2. Compute mean, median, variance, std for numeric columns.
3. Check for missing values and obvious outliers (don't need to fully treat them yet — just report).
4. Univariate plots (histograms, boxplots) and at least one bivariate plot (scatter, correlation heatmap).
5. One basic probability exercise on the data (e.g. probability of survival given class, using the Titanic example, or an equivalent conditional-frequency question for your dataset).
6. Write 5–8 bullet-point insights in plain English.

## Deliverable
- `notebooks/eda.ipynb` — the analysis
- `data/` — the raw CSV (or a script that downloads it)
- A short **Insights** section at the bottom of the notebook (or a separate `INSIGHTS.md`)

## Done when
Notebook runs top-to-bottom without errors, and the insights section answers
"what does this data actually tell us?" in your own words.
