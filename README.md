# Machine Learning Pipeline – Training & Batch Inference

This repository contains the **machine learning implementation and pipelines**
for the California Housing Price Prediction project.

All experimentation was first performed in notebooks.
Based on those experiments, the **final validated model and preprocessing logic**
were migrated into **production-grade Python pipelines**.

This README focuses on:

* How the ML pipelines are structured
* How to run training and inference
* What artifacts are produced
* What modeling decisions were finalized



## 📌 Final Modeling Decision

Multiple models were evaluated during experimentation, including:

* Linear Regression
* Ridge Regression
* Decision Trees
* Random Forest
* Gradient Boosting

Based on **hold-out evaluation and cross-validation results**,
**Gradient Boosting (`HistGradientBoostingRegressor`) with engineered features**
consistently achieved the best generalization performance.

👉 As a result:

* Only the **final Gradient Boosting model**
* And its required preprocessing steps

were migrated into Python pipelines for training and inference.

All other models remain documented in notebooks for reference.



## 🧠 Feature Processing Overview

The following preprocessing steps are applied consistently during
training and inference:

* Missing value imputation (`total_bedrooms`)
* One-hot encoding (`ocean_proximity`)
* Feature engineering:

  * Rooms per household
  * Bedrooms per room
  * Population per household

The same logic is reused across:

* Training
* Batch inference
* (Later) online inference

This ensures **no training–serving skew**.



## 🧪 Environment Setup

Create and activate a Python environment, then install dependencies:

```bash
pip install -r requirements.txt
export PYTHONPATH=$(pwd)/src
```

(At this stage, requirements include only ML and pipeline dependencies.)



## ⚙️ Training Pipeline

### Entry point

```bash
python -m pipelines.train
```

### What the training pipeline does

* Loads the raw California Housing dataset
* Splits data into train and test sets
* Applies preprocessing and feature engineering
* Trains the Gradient Boosting regression model
* Evaluates performance on train and test data
* Saves all required artifacts for inference

### Artifacts produced

Saved under:

```
artifacts/production/
```

Includes:

* Trained model
* Imputer
* Encoder
* Evaluation metrics (JSON)

These artifacts represent the **single source of truth** for inference.



## 🔁 Batch Inference Pipeline

### Preparing inference data

A utility script is provided to generate a sample inference dataset:

```bash
python data/inference/generate_sample.py
```

This creates:

```
data/inference/sample_input.csv
```

You can edit or extend this file to test different inference scenarios.


### Running batch inference

```bash
python -m pipelines.inference
```

### What the inference pipeline does

* Loads production artifacts
* Reads inference input data
* Applies the same preprocessing as training
* Runs predictions using the trained model
* Writes outputs to a separate directory

### Outputs

```
outputs/predictions.json
```

Inference outputs are kept separate from model artifacts to avoid
accidental coupling.



## 🗂️ ML-Relevant Repository Structure

```
CaliforniaHousePricePred
├── artifacts/
│   ├── experiments/         # Notebook experiment outputs
│   └── production/          # Final ML artifacts for inference
├── data/
│   ├── raw/                 # Original dataset
│   └── inference/           # Inference inputs & generators
├── notebooks/               # ML experimentation and analysis
├── pipelines/               # Train & batch inference entry points
├── src/
│   ├── preprocessing/       # Imputation, encoding, feature engineering
│   ├── models/              # Training & evaluation logic
│   └── inference/           # Shared inference utilities
├── outputs/                 # Batch inference results
└── logs/                    # Training & inference logs
```



## 🧩 Key Design Choices

* Notebook code is **not reused directly**
* All reusable logic lives in `src/`
* Pipelines are deterministic and scriptable
* Training and inference share identical preprocessing
* Artifacts are immutable once produced

---

