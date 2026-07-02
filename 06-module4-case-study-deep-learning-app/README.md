# 6. Module 4 Case Study — Deep Learning App

**Module:** 4 (Day 10) · **Type:** Case Study

## Objective
Build a real deep learning project covering neural network fundamentals through
transfer learning and optimization — the first "real" DL system in the program.

## Prerequisite skills
Perceptron/NN basics, activation functions, TensorFlow/Keras, CNNs, RNNs, LSTMs,
transfer learning (ResNet/VGG), dropout/batch norm, GPU training.

## Dataset
Pick ONE track (image or sequence) so the project stays scoped:
- **Image track:** CIFAR-10, Fashion-MNIST, or a small Kaggle image classification set
- **Sequence track:** a text dataset (e.g. IMDB reviews) or a time-series dataset (e.g. stock/weather data)

## Tasks
1. Build a simple feed-forward NN baseline in Keras; train and record accuracy/loss.
2. Build the architecture matching your track: CNN (image) or RNN/LSTM (sequence/time-series).
3. Apply dropout and batch normalization; compare metrics before/after.
4. For the image track: fine-tune a pretrained model (ResNet or VGG) via transfer
   learning and compare against your from-scratch CNN.
5. Train on GPU if available (Colab is fine); note training time difference vs. CPU.
6. Plot training/validation loss & accuracy curves; diagnose over/underfitting.

## Deliverable
- `notebooks/deep_learning_case_study.ipynb` — full training run with curves and comparisons
- `src/model.py` — final model architecture as a script
- Saved model weights (`.h5` or `SavedModel` dir) — can be excluded from Git via `.gitignore` if large

## Done when
You can point to a before/after comparison (baseline NN vs. tuned CNN/RNN vs.
transfer learning, as applicable) with numbers, not just "it worked."
