"""Shared prediction logic for the loan-approval app.

Kept separate from the Streamlit UI (`app.py`) so the exact same
feature-building + prediction code can be reused and tested from
`notebooks/sanity_check.ipynb` -- one source of truth, no duplicated logic.
"""
import pathlib

import joblib
import pandas as pd

MODEL_PATH = pathlib.Path(__file__).resolve().parent.parent / "model.pkl"

FEATURE_COLS = ["Married", "Education", "LoanAmount", "Credit_History",
                 "Area_Rural", "Area_Semiurban", "Area_Urban"]

# The model (from project 4) was trained on LoanAmount *after* project 2's
# preprocessing pipeline standardised it (mean 0, std 1). A person typing in
# a plain loan amount (e.g. "150", meaning thousands) needs that same
# transformation applied before the model sees it. These two numbers are the
# exact mean/std project 2's pipeline computed over the cleaned training
# data -- verified to reproduce project 2's scaled column exactly.
LOAN_AMOUNT_MEAN = 144.70210097719868
LOAN_AMOUNT_STD = 78.58157040808537


def load_model(path: pathlib.Path = MODEL_PATH):
    return joblib.load(path)


def build_feature_row(married: bool, graduate: bool, loan_amount_thousands: float,
                       good_credit_history: bool, property_area: str) -> pd.DataFrame:
    """Turn plain-English form answers into the one-row DataFrame the model expects."""
    if property_area not in ("Rural", "Semiurban", "Urban"):
        raise ValueError(f"property_area must be Rural/Semiurban/Urban, got {property_area!r}")
    if loan_amount_thousands <= 0:
        raise ValueError("Loan amount must be a positive number")

    scaled_loan_amount = (loan_amount_thousands - LOAN_AMOUNT_MEAN) / LOAN_AMOUNT_STD

    row = {
        "Married": int(married),
        "Education": int(graduate),
        "LoanAmount": scaled_loan_amount,
        "Credit_History": 1.0 if good_credit_history else 0.0,
        "Area_Rural": int(property_area == "Rural"),
        "Area_Semiurban": int(property_area == "Semiurban"),
        "Area_Urban": int(property_area == "Urban"),
    }
    return pd.DataFrame([row], columns=FEATURE_COLS)


def predict(model, feature_row: pd.DataFrame):
    """Return (predicted_label, probability_of_approval)."""
    prediction = model.predict(feature_row)[0]
    probability_approved = model.predict_proba(feature_row)[0][1]
    label = "Approved" if prediction == 1 else "Not Approved"
    return label, probability_approved
