"""Model architectures and training helpers for the Fashion-MNIST deep
learning case study.

Fashion-MNIST: 70,000 small (28x28 grayscale) photos of clothing, in 10
categories (T-shirt, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker,
Bag, Ankle boot). The goal in every model below is the same: look at a photo,
say which of the 10 categories it is.

Framework note: the course curriculum names TensorFlow/Keras, but TensorFlow
does not yet publish a build for this machine's Python version (3.14). We use
PyTorch instead -- the underlying concepts (layers, activations, dropout,
batch norm, transfer learning) are identical, just different code syntax.
"""
import time

import torch
import torch.nn as nn
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader, Subset

NUM_CLASSES = 10
CLASS_NAMES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
                "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def get_data_loaders(data_dir="../data", batch_size=128,
                      train_subset=None, test_subset=None):
    """Plain 28x28 grayscale tensors, for the feed-forward NN and CNNs."""
    transform = transforms.ToTensor()
    train_ds = torchvision.datasets.FashionMNIST(data_dir, train=True, download=True, transform=transform)
    test_ds = torchvision.datasets.FashionMNIST(data_dir, train=False, download=True, transform=transform)

    if train_subset:
        train_ds = Subset(train_ds, range(train_subset))
    if test_subset:
        test_ds = Subset(test_ds, range(test_subset))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader


def get_transfer_data_loaders(data_dir="../data", batch_size=32,
                                train_subset=3000, test_subset=1000, image_size=64):
    """Resized to 3-channel RGB, for the pretrained ResNet (which expects
    colour images, not single-channel grayscale). Subsampled + shrunk
    resolution (vs. ResNet's usual 224x224) so training stays feasible on a
    CPU-only machine."""
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
    ])
    train_ds = torchvision.datasets.FashionMNIST(data_dir, train=True, download=True, transform=transform)
    test_ds = torchvision.datasets.FashionMNIST(data_dir, train=False, download=True, transform=transform)

    train_ds = Subset(train_ds, range(train_subset))
    test_ds = Subset(test_ds, range(test_subset))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class SimpleNN(nn.Module):
    """Baseline: a plain feed-forward network. Flattens the image into one
    long list of pixel values -- no notion of "nearby pixels" at all."""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, 128),
            nn.ReLU(),
            nn.Linear(128, NUM_CLASSES),
        )

    def forward(self, x):
        return self.net(x)


class SimpleCNN(nn.Module):
    """A basic convolutional network -- looks at small local patches of the
    image (edges, textures) before deciding on a category. No dropout/batch
    norm yet -- that's the next model."""
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, NUM_CLASSES),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


class RegularizedCNN(nn.Module):
    """Same architecture as SimpleCNN, plus Batch Normalization (keeps the
    numbers flowing through the network well-behaved) and Dropout (randomly
    "turns off" some neurons during training so the network can't just
    memorise the training images)."""
    def __init__(self, dropout_p=0.3):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(dropout_p),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Dropout(dropout_p),
            nn.Linear(128, NUM_CLASSES),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


def build_transfer_model():
    """A ResNet18, pretrained on 1.2 million real-world photos (ImageNet),
    with its body frozen and only its final layer retrained to recognise our
    10 clothing categories instead. "Transfer learning" = reusing what it
    already learned about edges/shapes/textures instead of starting blank."""
    weights = torchvision.models.ResNet18_Weights.DEFAULT
    model = torchvision.models.resnet18(weights=weights)
    for param in model.parameters():
        param.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)  # this new layer trains
    return model


# ---------------------------------------------------------------------------
# Training / evaluation
# ---------------------------------------------------------------------------
def evaluate(model, loader, device, criterion):
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
            total += images.size(0)
    return total_loss / total, correct / total


def train_model(model, train_loader, test_loader, epochs=5, lr=1e-3, device="cpu"):
    """Generic training loop. Returns a history dict of per-epoch metrics so
    we can plot loss/accuracy curves afterwards."""
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=lr)

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    for epoch in range(epochs):
        model.train()
        running_loss, correct, total = 0.0, 0, 0
        t0 = time.time()
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
            total += images.size(0)

        train_loss, train_acc = running_loss / total, correct / total
        val_loss, val_acc = evaluate(model, test_loader, device, criterion)

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)

        print(f"Epoch {epoch+1}/{epochs} ({time.time()-t0:.1f}s) -- "
              f"train_loss={train_loss:.3f} train_acc={train_acc:.3f} "
              f"val_loss={val_loss:.3f} val_acc={val_acc:.3f}")

    return history
