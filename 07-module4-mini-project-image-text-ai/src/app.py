"""Streamlit app: upload a photo of a clothing item and get an instant
prediction from the model trained in project 6.

Run it:
    streamlit run src/app.py
"""
import pathlib

import pandas as pd
import streamlit as st
from PIL import Image

from inference import load_model, predict_image

SAMPLES_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "samples"
FAILURES_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "failure_examples"

st.set_page_config(page_title="Clothing Classifier")

st.title("Clothing Classifier")
st.write(
    "Upload a photo of a single clothing item and this app will guess which "
    "of 10 categories it belongs to (T-shirt, Trouser, Pullover, Dress, Coat, "
    "Sandal, Shirt, Sneaker, Bag, or Ankle boot). It's powered by the CNN "
    "trained in project 6 on the Fashion-MNIST dataset."
)
st.caption(
    "Known limitation: this model was trained on small, centered, "
    "high-contrast 28x28 photos with plain backgrounds. Real photos taken "
    "on a phone (cluttered background, odd angle, colour) may confuse it "
    "far more than the clean example images below."
)


@st.cache_resource
def get_model():
    return load_model()


model = get_model()


def show_prediction(image: Image.Image):
    result = predict_image(image, model)
    st.image(image, caption="Input image", width=150)
    st.success(f"Predicted: **{result['predicted_label']}** (confidence: {result['confidence']:.0%})")
    probs = pd.Series(result["all_probabilities"]).sort_values(ascending=False)
    st.bar_chart(probs)


tab1, tab2 = st.tabs(["Upload your own image", "Try example images"])

with tab1:
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        show_prediction(Image.open(uploaded_file))

with tab2:
    st.write("A mix of examples the model gets right, and a few it gets wrong (documented failure cases):")
    sample_files = sorted(SAMPLES_DIR.glob("*.png")) + sorted(FAILURES_DIR.glob("*.png"))
    chosen_name = st.selectbox("Pick an example", [f.name for f in sample_files])
    chosen_path = next(f for f in sample_files if f.name == chosen_name)
    show_prediction(Image.open(chosen_path))
    if chosen_path.parent.name == "failure_examples":
        st.warning("This is one of the model's documented failure cases -- its guess may not match the true label.")
