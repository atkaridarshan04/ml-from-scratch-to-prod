# ML from Scratch to Production

An end-to-end **Machine Learning engineering and MLOps project** that demonstrates
how to design, train, validate, and operationalize a machine learning model using
**industry-standard, production-oriented ML practices**.

The project uses the **California Housing dataset** as a reference use case and
focuses on building a **reproducible, maintainable, and deployment-ready ML system**
— progressing from experimentation to production pipelines.

---

## 🎯 Project Objective

The objectives of this project are to:

- Engineer a regression model **from first principles**
- Follow a **structured ML lifecycle** from data understanding to validation
- Establish a **validated baseline model**
- Migrate notebook-based experimentation into **production-grade Python pipelines**
- Build the foundation for a **full MLOps workflow** (CI/CD, tracking, deployment)

---

## 🧠 Machine Learning Phase (Completed)

The ML phase was implemented using a **progressive, evidence-driven approach**, where
each modeling decision was backed by quantitative evaluation.

### 1️⃣ Problem Framing & Data Understanding
- Defined prediction target: `median_house_value`
- Dataset and feature analysis
- Identification of numerical vs categorical features
- Constraints and data quality considerations

### 2️⃣ Baseline Modeling
- Linear Regression
- Ridge Regression
- Used to diagnose bias, variance, and scaling behavior

### 3️⃣ Non-Linear Modeling
- Decision Trees (unconstrained & constrained)
- Random Forest for variance reduction and stability

### 4️⃣ Feature Engineering
- Domain-driven engineered features:
  - Rooms per household
  - Bedrooms per room
  - Population per household
- Systematic evaluation across model families

### 5️⃣ Advanced Modeling
- Gradient Boosting using `HistGradientBoostingRegressor`
- Selected after Random Forest performance plateaued
- Improved bias–variance tradeoff

### 6️⃣ Model Validation
- Hold-out test evaluation
- Cross-validation for stability
- Metrics: RMSE and R²

👉 **Gradient Boosting with engineered features is selected as the current production baseline.**

---

## 📊 Current Best Model

| Model | Test RMSE (≈) | CV RMSE (≈) | Notes |
|------|---------------|------------|------|
| Random Forest | ~49k | ~49k | Stable non-linear baseline |
| Gradient Boosting | **~45.5k** | **~46.5k** | Lower bias, improved generalization |

Cross-validation confirms consistent generalization across data splits.

---

## ⚙️ Production Pipelines (Completed)

Notebook experimentation has been **fully migrated to production-grade pipelines**.

### ✅ Training Pipeline
- Deterministic data splitting
- Feature preprocessing (imputation, encoding, feature engineering)
- Model training and evaluation
- Artifact persistence (model, preprocessors, metrics)
- Structured logging

### ✅ Batch Inference Pipeline
- Loads production artifacts
- Applies identical preprocessing as training
- Runs predictions on curated inference inputs
- Outputs predictions separately from model artifacts

These pipelines are designed to be:
- CI/CD friendly
- Reproducible
- API-ready

---

## 🗂️ Repository Structure

```

CaliforniaHousePricePred
├── artifacts/
│   ├── experiments/         # Notebook experiment outputs (history)
│   └── production/          # Single source of truth for deployment
├── data/
│   ├── raw/                 # Original dataset
│   └── inference/           # Curated inference inputs
├── docs/                    # Design decisions & ML reasoning
├── notebooks/               # Exploratory ML experimentation
├── pipelines/               # Training & inference execution entry points
├── src/                     # Reusable production ML code
├── outputs/                 # Inference outputs (ephemeral)
├── logs/                    # Pipeline execution logs
├── requirements.txt
└── README.md

```

---

## 📄 Documentation Philosophy

- **Notebooks** → exploration and experimentation
- **Docs** → reasoning, decisions, and conclusions
- **Pipelines** → execution and orchestration
- **Source code** → reusable, testable ML components
- **Artifacts** → immutable, versioned model outputs
- **Outputs** → ephemeral inference results

---

## 🚀 MLOps Phase (Next)

The next phase focuses on **serving and automation**:

- FastAPI-based online inference
- CI/CD integration for training and inference pipelines
- MLflow experiment tracking and model registry
- Champion–challenger model promotion
- Monitoring and retraining strategies

The current pipelines serve as a **stable and production-ready foundation** for
these MLOps components.

---

## 🧩 Design Principles

- Sequential ML development (baseline → validation → improvement)
- Clear separation of experimentation and production code
- Reproducibility and traceability at every stage
- Evidence-based model selection
- Infrastructure-agnostic ML design

---

## 📌 Summary

This repository demonstrates how to evolve a machine learning project from
notebook-based experimentation into a **clean, maintainable, and production-ready
ML system**, following real-world ML engineering and MLOps best practices.

