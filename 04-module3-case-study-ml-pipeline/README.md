# 4. Module 3 Case Study — End-to-End ML Pipeline

**Module:** 3 (Day 11) · **Type:** Case Study

## Objective
Build a complete supervised-learning workflow: multiple model types, proper
evaluation, cross-validation, and hyperparameter tuning — not just a single
`.fit()`/`.predict()` call.

## Prerequisite skills
Regression, classification, KNN, decision trees, random forest, evaluation
metrics (accuracy/precision/recall), k-fold cross-validation, bias-variance,
grid search.

## Dataset
Use the cleaned dataset from project 2, or pick a fresh one with a clear
target column (classification or regression) — e.g. Titanic (survival),
House Prices (price), or Wine Quality.

## Tasks
1. Split into train/test (and hold out a validation fold or use k-fold CV throughout).
2. Train at least 3 model types: e.g. Logistic/Linear Regression, KNN, Random Forest.
3. Evaluate each with the appropriate metrics (accuracy/precision/recall/F1 for
   classification; RMSE/R² for regression).
4. Apply k-fold cross-validation and compare CV score vs. single train/test split.
5. Diagnose over/underfitting for at least one model (learning curve or
   train-vs-test score gap) and adjust.
6. Run `GridSearchCV` (or `RandomizedSearchCV`) on the best-performing model
   and report the tuned parameters.
7. Wrap the final chosen model + preprocessing into one pipeline (`sklearn.pipeline.Pipeline`).

## Deliverable
- `notebooks/ml_pipeline.ipynb` — full workflow with metric comparisons across models
- `src/train.py` — script version that trains and saves the final tuned model (`model.pkl`)
- A short results table: model vs. metrics vs. CV score

## Done when
`src/train.py` runs standalone and produces a saved model plus printed metrics
matching the notebook.
