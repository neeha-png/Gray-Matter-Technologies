# 7. Module 4 Mini Project — Image/Text AI Application

**Module:** 4 (Day 11) · **Type:** Mini Project

## Objective
Package the modeling work from project 6 into a small, usable AI application
(not just a training notebook).

## Prerequisite skills
Same as project 6, plus basic inference/serving (loading a saved model and
running it on new input).

## Requirements
- The trained model from project 6
- `streamlit` or a minimal script-based CLI for inference
- For images: a few sample images not used in training, to demo on
- For text: a few sample sentences/reviews to demo on

## Tasks
1. Load the saved model from project 6.
2. Write an inference function: image in → predicted class + confidence out
   (or text in → predicted label/sentiment out).
3. Build a tiny front end: Streamlit file-uploader (image track) or text box
   (text track) that calls the inference function and displays the result.
4. Test with at least 5 out-of-training examples and sanity-check the outputs.
5. Note failure cases (things it gets wrong) — this matters more than a perfect demo.

## Deliverable
- `src/app.py` — the demo application
- `src/inference.py` — the inference function, separated from UI code
- `notebooks/` — optional scratch notebook for testing inference before wiring the UI

## Done when
You can upload/type a new example and get a prediction back through the app,
and you have at least one documented example where the model is wrong.
