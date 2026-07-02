"""Streamlit app: a simple, non-technical way to get a loan-approval prediction
from the model trained in project 4.

Run it:
    streamlit run src/app.py
"""
import streamlit as st

from predict import build_feature_row, load_model, predict

st.set_page_config(page_title="Loan Approval Predictor", page_icon=None)

st.title("Loan Approval Predictor")
st.write(
    "Fill in an applicant's details below and get an instant prediction of "
    "whether a home loan would likely be approved. This is powered by the "
    "model trained in project 4 on 614 real past loan applications."
)


@st.cache_resource
def get_model():
    return load_model()


model = get_model()

with st.form("loan_form"):
    married = st.selectbox("Are you married?", ["Yes", "No"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    loan_amount = st.number_input(
        "Loan amount requested (in thousands, e.g. 150 = 150,000)",
        min_value=1.0, max_value=1000.0, value=150.0, step=1.0,
    )
    credit_history = st.selectbox(
        "Credit history",
        ["Good (paid past debts on time)", "Poor / no credit history"],
    )
    property_area = st.selectbox("Property area", ["Rural", "Semiurban", "Urban"])
    submitted = st.form_submit_button("Get prediction")

if submitted:
    try:
        row = build_feature_row(
            married=(married == "Yes"),
            graduate=(education == "Graduate"),
            loan_amount_thousands=loan_amount,
            good_credit_history=(credit_history.startswith("Good")),
            property_area=property_area,
        )
        label, probability_approved = predict(model, row)

        if label == "Approved":
            st.success(f"Likely **Approved** (estimated probability: {probability_approved:.0%})")
        else:
            st.error(f"Likely **Not Approved** (estimated probability of approval: {probability_approved:.0%})")

        st.caption(
            "Reminder from our earlier analysis: credit history is by far the "
            "biggest factor in this model's decision -- far more than loan "
            "amount, education, or where the property is."
        )
    except ValueError as e:
        st.warning(f"Please check your input: {e}")
