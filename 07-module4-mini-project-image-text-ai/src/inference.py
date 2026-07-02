"""Inference logic for the clothing classifier, kept separate from the UI
(`app.py`) so it can be tested on its own -- from a notebook, a script, or
the app -- without duplicating the "how do I turn an image into a
prediction" logic in more than one place.
"""
import pathlib
import sys

import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

# Reuse project 6's architecture code directly rather than re-declaring the
# same class here (one source of truth for what "RegularizedCNN" means).
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent
                     / "06-module4-case-study-deep-learning-app" / "src"))
import model as m6  # noqa: E402

MODEL_PATH = pathlib.Path(__file__).resolve().parent.parent / "best_model.pt"
CLASS_NAMES = m6.CLASS_NAMES

_preprocess = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
])


def load_model(path: pathlib.Path = MODEL_PATH):
    model = m6.RegularizedCNN(dropout_p=0.3)
    state_dict = torch.load(path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model


def predict_image(image: Image.Image, model) -> dict:
    """image -> predicted class name, confidence, and the full probability
    breakdown across all 10 categories."""
    tensor = _preprocess(image).unsqueeze(0)  # add batch dimension
    with torch.no_grad():
        logits = model(tensor)
        probabilities = F.softmax(logits, dim=1)[0]

    predicted_idx = int(probabilities.argmax())
    return {
        "predicted_label": CLASS_NAMES[predicted_idx],
        "confidence": float(probabilities[predicted_idx]),
        "all_probabilities": {name: float(p) for name, p in zip(CLASS_NAMES, probabilities)},
    }
