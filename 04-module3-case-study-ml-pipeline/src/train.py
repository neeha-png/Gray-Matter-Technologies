"""End-to-end ML training script for the loan-approval prediction problem.

Reuses the already-cleaned dataset from project 2
(`02-module2-case-study-preprocessing/data/processed/loan_processed.csv`) --
this project is about the modelling workflow, not re-cleaning data.

Run standalone:
    python src/train.py
"""
import pathlib

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = (
    PROJECT_ROOT.parent
    / "02-module2-case-study-preprocessing"
    / "data" / "processed" / "loan_processed.csv"
)
MODEL_PATH = PROJECT_ROOT / "model.pkl"

FEATURE_COLS = ["Married", "Education", "LoanAmount", "Credit_History",
                 "Area_Rural", "Area_Semiurban", "Area_Urban"]
TARGET_COL = "Loan_Status"


def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    return X, y


def candidate_models():
    """Three different model types, each wrapped with the same scaler."""
    return {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=42)),
        ]),
        "KNN": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", KNeighborsClassifier()),
        ]),
        "Random Forest": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(random_state=42)),
        ]),
    }


def evaluate(pipeline, X_train, y_train, X_test, y_test):
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
    }


def cross_validate(pipeline, X, y, cv_folds=5):
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring="accuracy")
    return scores.mean(), scores.std()


def diagnose_overfitting(pipeline, X_train, y_train, X_test, y_test):
    """Compare train vs test accuracy for a fitted pipeline -- a big gap
    (train much higher than test) signals overfitting."""
    pipeline.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, pipeline.predict(X_train))
    test_acc = accuracy_score(y_test, pipeline.predict(X_test))
    return train_acc, test_acc


def tune_random_forest(X_train, y_train):
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(random_state=42)),
    ])
    param_grid = {
        "clf__n_estimators": [100, 200],
        "clf__max_depth": [3, 5, 8, None],
        "clf__min_samples_leaf": [1, 3, 5],
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(pipeline, param_grid, cv=cv, scoring="f1")
    grid.fit(X_train, y_train)
    return grid


def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    results = []
    for name, pipeline in candidate_models().items():
        metrics = evaluate(pipeline, X_train, y_train, X_test, y_test)
        cv_mean, cv_std = cross_validate(pipeline, X, y)
        results.append({"model": name, **metrics, "cv_accuracy_mean": cv_mean, "cv_accuracy_std": cv_std})

    results_df = pd.DataFrame(results).set_index("model")
    print("=== Baseline model comparison ===")
    print(results_df.round(3))

    rf_pipeline = candidate_models()["Random Forest"]
    train_acc, test_acc = diagnose_overfitting(rf_pipeline, X_train, y_train, X_test, y_test)
    print(f"\n=== Overfitting check (default Random Forest) ===")
    print(f"Train accuracy: {train_acc:.3f} | Test accuracy: {test_acc:.3f} | Gap: {train_acc - test_acc:.3f}")

    print("\n=== Tuning Random Forest with GridSearchCV ===")
    grid = tune_random_forest(X_train, y_train)
    print(f"Best params: {grid.best_params_}")
    print(f"Best CV F1 score: {grid.best_score_:.3f}")

    tuned_train_acc = accuracy_score(y_train, grid.predict(X_train))
    tuned_test_acc = accuracy_score(y_test, grid.predict(X_test))
    print(f"Tuned model -- train accuracy: {tuned_train_acc:.3f} | test accuracy: {tuned_test_acc:.3f}")

    final_metrics = evaluate(grid.best_estimator_, X_train, y_train, X_test, y_test)
    print("\n=== Final tuned model metrics on test set ===")
    for k, v in final_metrics.items():
        print(f"  {k}: {v:.3f}")

    joblib.dump(grid.best_estimator_, MODEL_PATH)
    print(f"\nSaved final tuned model -> {MODEL_PATH}")


if __name__ == "__main__":
    main()
