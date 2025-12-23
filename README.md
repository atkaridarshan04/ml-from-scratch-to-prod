# ML from Scratch to Production

An end-to-end **Machine Learning engineering and MLOps project** that demonstrates
how to design, train, validate, and operationalize a machine learning model using
**industry-standard, production-oriented ML practices**.

The project uses the **California Housing dataset** as a reference use case and
focuses on building a **reproducible, maintainable, and deployment-ready ML system**
— progressing from experimentation to training pipelines, inference pipelines, and
a production-grade online inference API.

---

## 🎯 Project Objective

The objectives of this project are to:

* Engineer a regression model **from first principles**
* Follow a **structured ML lifecycle** from data understanding to validation
* Establish a **validated baseline model**
* Migrate notebook-based experimentation into **production-grade Python pipelines**
* Build a **production-ready inference service** for real-time predictions
* Lay the foundation for a **full MLOps workflow** (CI/CD, tracking, deployment)

---

## 🧠 Machine Learning Phase (Completed)

The ML phase was implemented using a **progressive, evidence-driven approach**, where
each modeling decision was backed by quantitative evaluation.

### 1️⃣ Problem Framing & Data Understanding

* Defined prediction target: `median_house_value`
* Dataset and feature analysis
* Identification of numerical vs categorical features
* Constraints and data quality considerations

### 2️⃣ Baseline Modeling

* Linear Regression
* Ridge Regression
* Used to diagnose bias, variance, and scaling behavior

### 3️⃣ Non-Linear Modeling

* Decision Trees (unconstrained & constrained)
* Random Forest for variance reduction and stability

### 4️⃣ Feature Engineering

* Domain-driven engineered features:

  * Rooms per household
  * Bedrooms per room
  * Population per household
* Systematic evaluation across model families

### 5️⃣ Advanced Modeling

* Gradient Boosting using `HistGradientBoostingRegressor`
* Selected after Random Forest performance plateaued
* Improved bias–variance tradeoff

### 6️⃣ Model Validation

* Hold-out test evaluation
* Cross-validation for stability
* Metrics: RMSE and R²

👉 **Gradient Boosting with engineered features is selected as the current production baseline.**

---

## 📊 Current Best Model

| Model             | Test RMSE (≈) | CV RMSE (≈) | Notes                               |
| ----------------- | ------------- | ----------- | ----------------------------------- |
| Random Forest     | ~49k          | ~49k        | Stable non-linear baseline          |
| Gradient Boosting | **~45.5k**    | **~46.5k**  | Lower bias, improved generalization |

Cross-validation confirms consistent generalization across data splits.

---

## ⚙️ Production Pipelines (Completed)

Notebook experimentation has been **fully migrated to production-grade pipelines**.

### ✅ Training Pipeline

* Deterministic data splitting
* Feature preprocessing (imputation, encoding, feature engineering)
* Model training and evaluation
* Artifact persistence (model, preprocessors, metrics)
* Structured logging

### ✅ Batch Inference Pipeline

* Loads production artifacts
* Applies identical preprocessing as training
* Runs predictions on curated inference inputs
* Outputs predictions separately from model artifacts

These pipelines are designed to be:

* Reproducible
* CI/CD friendly
* Aligned with online inference behavior

---

## 🌐 Online Inference API (Completed)

A **production-ready FastAPI service** has been implemented to serve the trained
model for **real-time predictions**.

### Key characteristics:

* FastAPI-based REST API
* Request/response validation using Pydantic schemas
* Single-load artifact initialization using FastAPI lifespan events
* Identical preprocessing logic shared with training and batch inference
* Structured, file-based logging for API lifecycle and inference
* Automated API tests (health, prediction, validation)
* Fully containerized using Docker

### Available endpoints:

* `GET /health` — service health check
* `POST /predict` — run online housing price predictions

The API is designed to be:

* Stateless
* Deterministic
* Deployment-ready (Docker-compatible)
* Safe for CI/CD and cloud environments

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
├── pipelines/               # Training & batch inference entry points
├── src/                     # Reusable production ML & API code
├── tests/                   # Automated API tests
├── outputs/                 # Ephemeral inference outputs
├── logs/                    # Pipeline and API logs
├── Dockerfile               # Inference service containerization
├── requirements/            # Split dependencies (base / train / api)
└── README.md
```


---

## 🚀 MLOps Phase (Next)

The next phase focuses on **automation and deployment maturity**:

* CI/CD pipelines for training and API builds
* Container registry integration
* MLflow experiment tracking and model registry
* Champion–challenger model promotion
* Monitoring, alerting, and retraining strategies

The current system provides a **stable, production-ready foundation** for these
MLOps extensions.

---

## 🧩 Design Principles

* Sequential ML development (baseline → validation → improvement)
* Clear separation of experimentation, pipelines, and serving
* Reproducibility and traceability at every stage
* Evidence-based model selection
* Infrastructure-agnostic ML system design

---

## 📌 Summary

This repository demonstrates how to evolve a machine learning project from
notebook-based experimentation into a **fully operational ML system**, including:

* Validated model development
* Production-grade pipelines
* Online inference via a tested, containerized API
* A clear path toward end-to-end MLOps

---