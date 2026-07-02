"""Review Triage Assistant -- an end-user-facing app that calls project 8's
live sentiment API in real time. This app has no model logic of its own; it
only talks to the API over HTTP, the same way any real product would.

Requires project 8's API to be running:
    python ../08-module5-case-study-industry-application/src/api.py

Then run this app:
    streamlit run src/app.py
"""
import requests
import streamlit as st

API_URL = "http://localhost:5000"

EXAMPLE_REVIEWS = {
    "-- pick an example --": "",
    "Happy customer": "This exceeded my expectations, works perfectly and arrived early!",
    "Angry customer": "This broke after two days and support never replied to my emails.",
    "Neutral / mixed": "It's fine I guess, does what it says but nothing special.",
}

st.set_page_config(page_title="Review Triage Assistant")

st.title("Review Triage Assistant")
st.write(
    "Paste a customer review below and this tool will instantly flag whether "
    "it needs a team member's attention -- so support staff can focus on "
    "unhappy customers first instead of reading every review in order."
)

example_choice = st.selectbox("Try an example review", list(EXAMPLE_REVIEWS.keys()))
default_text = EXAMPLE_REVIEWS[example_choice]

review_text = st.text_area("Customer review", value=default_text, height=100)
analyze_clicked = st.button("Analyze this review")

if analyze_clicked:
    if not review_text or not review_text.strip():
        st.warning("Please enter or select a review first.")
    else:
        with st.spinner("Checking review..."):
            try:
                response = requests.post(f"{API_URL}/predict", json={"text": review_text}, timeout=5)
            except requests.exceptions.ConnectionError:
                st.error(
                    "We couldn't reach the review-checking service. Make sure "
                    "project 8's API is running, then try again."
                )
                response = None

        if response is not None:
            if response.status_code != 200:
                st.warning(f"The service couldn't process that review: {response.json().get('error', 'unknown error')}")
            else:
                result = response.json()
                sentiment = result["sentiment"]
                confidence = result["confidence"]

                if confidence < 0.65:
                    confidence_note = "though it isn't very confident -- a human may want to double-check"
                elif confidence < 0.85:
                    confidence_note = "with reasonable confidence"
                else:
                    confidence_note = "with high confidence"

                if sentiment == "negative":
                    st.error(f"**Needs attention** -- this customer seems unhappy ({confidence_note}).")
                else:
                    st.success(f"**No action needed** -- this customer seems happy ({confidence_note}).")

                with st.expander("See the raw output behind this result"):
                    st.json(result)
