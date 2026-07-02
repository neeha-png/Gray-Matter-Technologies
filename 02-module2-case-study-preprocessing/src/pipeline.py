"""Reusable preprocessing pipeline for the Loan Prediction case study.

Two raw sources go in (a CSV of applicant demographics + a SQLite table of
loan financials), one clean, model-ready table comes out.

Run it directly to reproduce the processed dataset from the raw data:
    python src/pipeline.py
"""
import pathlib
import sqlite3

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

NUMERIC_COLS = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term"]
OUTLIER_CAP_QUANTILE = 0.99  # cap extreme incomes/amounts instead of dropping rows


# ---------------------------------------------------------------------------
# 1. Load from 2+ sources and merge
# ---------------------------------------------------------------------------
def load_raw(raw_dir: pathlib.Path = RAW_DIR) -> pd.DataFrame:
    """Load applicant demographics (CSV) + loan financials (SQLite), join on Loan_ID."""
    applicants = pd.read_csv(raw_dir / "applicants.csv")

    with sqlite3.connect(raw_dir / "loan_data.db") as conn:
        financials = pd.read_sql("SELECT * FROM loan_financials", conn)

    merged = applicants.merge(financials, on="Loan_ID", how="inner")
    return merged


# ---------------------------------------------------------------------------
# 2. Clean: impute missing values, treat outliers
# ---------------------------------------------------------------------------
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values and cap outliers.

    Rules (chosen after inspecting the raw data):
    - Categorical columns (Gender, Married, Dependents, Self_Employed,
      Loan_Amount_Term, Credit_History): fill with the most common value
      (mode). Credit_History and Loan_Amount_Term look numeric but only take
      a handful of discrete values, so they behave like categories.
    - LoanAmount: fill with the median, not the mean, because it's
      right-skewed (a few very large loans would drag the mean up).
    - ApplicantIncome / CoapplicantIncome / LoanAmount: cap (winsorize) at
      the 99th percentile rather than dropping rows, so a few extremely
      wealthy applicants don't distort scaling/PCA later but we don't throw
      away real data.
    """
    df = df.copy()

    mode_fill_cols = ["Gender", "Married", "Dependents", "Self_Employed",
                       "Loan_Amount_Term", "Credit_History"]
    for col in mode_fill_cols:
        df[col] = df[col].fillna(df[col].mode().iloc[0])

    df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())

    for col in ["ApplicantIncome", "CoapplicantIncome", "LoanAmount"]:
        cap = df[col].quantile(OUTLIER_CAP_QUANTILE)
        df[col] = df[col].clip(upper=cap)

    return df


# ---------------------------------------------------------------------------
# 3. Encode categoricals, scale numerics
# ---------------------------------------------------------------------------
def encode_and_scale(df: pd.DataFrame) -> pd.DataFrame:
    """Turn text categories into numbers and put numeric columns on the same scale.

    - Binary yes/no-style columns -> 0/1 (label encoding).
    - Dependents ("0","1","2","3+") -> 0/1/2/3 (ordinal, "3+" becomes 3).
    - Property_Area (3 unrelated categories) -> one-hot columns, since there's
      no natural order between Rural/Semiurban/Urban.
    - Numeric columns -> standardised (mean 0, std 1) so no single column
      dominates just because its raw numbers are bigger.
    """
    df = df.copy()

    df["Gender"] = df["Gender"].map({"Male": 1, "Female": 0})
    df["Married"] = df["Married"].map({"Yes": 1, "No": 0})
    df["Self_Employed"] = df["Self_Employed"].map({"Yes": 1, "No": 0})
    df["Education"] = df["Education"].map({"Graduate": 1, "Not Graduate": 0})
    df["Dependents"] = df["Dependents"].replace({"3+": "3"}).astype(int)
    df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

    df = pd.get_dummies(df, columns=["Property_Area"], prefix="Area", drop_first=False)
    area_cols = [c for c in df.columns if c.startswith("Area_")]
    df[area_cols] = df[area_cols].astype(int)

    scaler = StandardScaler()
    df[NUMERIC_COLS] = scaler.fit_transform(df[NUMERIC_COLS])

    return df


# ---------------------------------------------------------------------------
# 4. Correlation-based feature selection
# ---------------------------------------------------------------------------
def select_features(df: pd.DataFrame, target_col: str = "Loan_Status",
                     min_target_corr: float = 0.03,
                     max_pairwise_corr: float = 0.85) -> tuple[pd.DataFrame, dict]:
    """Drop features that barely relate to the target, or duplicate another feature.

    Two checks:
    1. Drop any feature whose correlation with the target is weaker than
       `min_target_corr` -- it's not carrying useful signal.
    2. For any pair of *remaining* features correlated with each other above
       `max_pairwise_corr`, drop whichever one has the weaker link to the
       target -- keeping both would just be double-counting the same signal.
    """
    id_cols = [c for c in ["Loan_ID"] if c in df.columns]
    feature_cols = [c for c in df.columns if c not in id_cols + [target_col]]

    corr_matrix = df[feature_cols + [target_col]].corr()
    target_corr = corr_matrix[target_col].drop(target_col)

    dropped = {}

    weak = target_corr[target_corr.abs() < min_target_corr].index.tolist()
    dropped.update({c: f"weak correlation with target ({target_corr[c]:.3f})" for c in weak})

    remaining = [c for c in feature_cols if c not in weak]
    feat_corr = df[remaining].corr().abs()
    for i, col_a in enumerate(remaining):
        if col_a in dropped:
            continue
        for col_b in remaining[i + 1:]:
            if col_b in dropped:
                continue
            if feat_corr.loc[col_a, col_b] > max_pairwise_corr:
                weaker = col_a if target_corr[col_a] < target_corr[col_b] else col_b
                dropped[weaker] = (
                    f"redundant with {col_b if weaker == col_a else col_a} "
                    f"(pairwise corr {feat_corr.loc[col_a, col_b]:.2f})"
                )

    kept = id_cols + [c for c in feature_cols if c not in dropped] + [target_col]
    return df[kept], dropped


# ---------------------------------------------------------------------------
# 5. PCA — compare explained variance for a few component counts
# ---------------------------------------------------------------------------
def apply_pca(df: pd.DataFrame, feature_cols: list[str],
               component_counts: tuple[int, ...] = (2, 3, 5)) -> pd.DataFrame:
    """Run PCA at a few different component counts and report variance explained."""
    X = df[feature_cols].to_numpy()
    rows = []
    for n in component_counts:
        pca = PCA(n_components=n, random_state=42)
        pca.fit(X)
        rows.append({
            "n_components": n,
            "explained_variance_ratio_per_component": np.round(pca.explained_variance_ratio_, 3).tolist(),
            "total_explained_variance": round(pca.explained_variance_ratio_.sum(), 3),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def run_pipeline(raw_dir: pathlib.Path = RAW_DIR,
                  processed_dir: pathlib.Path = PROCESSED_DIR) -> pd.DataFrame:
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw = load_raw(raw_dir)
    cleaned = clean(raw)
    encoded = encode_and_scale(cleaned)
    selected, dropped = select_features(encoded)

    selected.to_csv(processed_dir / "loan_processed.csv", index=False)

    print(f"Processed dataset: {selected.shape[0]} rows, {selected.shape[1]} columns")
    if dropped:
        print("Dropped features:")
        for col, reason in dropped.items():
            print(f"  - {col}: {reason}")
    print(f"Saved -> {processed_dir / 'loan_processed.csv'}")

    return selected


if __name__ == "__main__":
    run_pipeline()
