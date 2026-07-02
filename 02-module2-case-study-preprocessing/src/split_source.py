"""One-time setup script.

This project needs data coming from "2+ sources" to practice merging/joins.
The real-world Loan Prediction dataset (Analytics Vidhya / Dream Housing
Finance) naturally splits into two related tables:

- applicants.csv       -- who the person is (demographics)
- loan_financials.db   -- their loan application numbers (income, amount, status)

Run this once from the project root:
    python src/split_source.py

It downloads nothing itself -- it expects data/raw/loan_prediction_source.csv
to already exist (the full original file), and produces:
    data/raw/applicants.csv
    data/raw/loan_data.db   (SQLite, table "loan_financials")
"""
import pathlib
import sqlite3

import pandas as pd

RAW_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"
SOURCE = RAW_DIR / "loan_prediction_source.csv"

APPLICANT_COLS = [
    "Loan_ID", "Gender", "Married", "Dependents", "Education",
    "Self_Employed", "Property_Area",
]
FINANCIAL_COLS = [
    "Loan_ID", "ApplicantIncome", "CoapplicantIncome", "LoanAmount",
    "Loan_Amount_Term", "Credit_History", "Loan_Status",
]


def main():
    df = pd.read_csv(SOURCE)

    applicants = df[APPLICANT_COLS]
    applicants.to_csv(RAW_DIR / "applicants.csv", index=False)

    financials = df[FINANCIAL_COLS]
    db_path = RAW_DIR / "loan_data.db"
    with sqlite3.connect(db_path) as conn:
        financials.to_sql("loan_financials", conn, if_exists="replace", index=False)

    print(f"Wrote {RAW_DIR / 'applicants.csv'} ({applicants.shape})")
    print(f"Wrote {db_path} -> table 'loan_financials' ({financials.shape})")


if __name__ == "__main__":
    main()
