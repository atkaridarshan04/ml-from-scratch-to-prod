# ML from Scratch to Production (API Baseline)

This branch contains the **API baseline implementation**, where the online
inference service loads trained models and preprocessing artifacts directly
from the local filesystem (`artifacts/production`).

It represents the system state **before introducing MLflow-based model
registry and lifecycle management**, and is kept as a stable reference for
comparison with the production MLOps design in the `main` branch.


## 🎯 What This Branch Represents

This branch contains a **pre-MLflow production-style system**, including:

- Finalized ML training pipeline
- Batch inference pipeline
- FastAPI-based online inference service
- Local artifact management (`artifacts/production`)
- Shared preprocessing logic across training, batch inference, and API
- Automated API tests
- Dockerized inference service

This design serves as a **baseline architecture** before adopting a centralized
model registry and lifecycle management.



## 🧠 Machine Learning Overview

- Multiple model families were evaluated during experimentation
- Feature engineering was validated across models
- **Gradient Boosting (`HistGradientBoostingRegressor`)** achieved the best
  generalization performance
- This model was selected as the **production baseline**
- Finalized preprocessing and modeling logic was migrated into Python pipelines

### Detailed ML artifacts are available in:
- `notebooks/` — experimentation and EDA
- `docs/` — ML design, feature analysis, and modeling decisions
- `artifacts/experiments/` — historical experiment outputs

> **For only ml workflow refer the `ml-baseline` branch**



## 🗂️ Repository Structure (API Baseline)

```
root
├── artifacts/
│   ├── experiments/         # Historical experiment outputs
│   └── production/          # Deployment-ready ML artifacts
├── data/
│   ├── raw/                 # Original dataset
│   └── inference/           # Inference inputs & generators
├── docs/                    # ML design & decision records
├── notebooks/               # Experimentation history
├── outputs/                 # Batch inference outputs
├── pipelines/               # Training & batch inference entry points
├── requirements/            # Dependency split (train / api)
├── src/                     # Production ML & API code
├── tests/                   # API tests
├── Dockerfile               # Inference service containerization
└── README.md
```


## ⚙️ ML Pipelines

### Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install API dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements/train.txt

export PYTHONPATH=$(pwd)/src
```

### Training Pipeline

```bash
python -m pipelines.train
```

Responsibilities:

* Loads raw dataset
* Applies preprocessing and feature engineering
* Trains the final Gradient Boosting model
* Evaluates performance
* Saves trained artifacts locally

Artifacts are written to:

```
artifacts/production/
```

---

### Batch Inference Pipeline

```bash
python -m pipelines.inference
```

Responsibilities:

* Loads production artifacts from the filesystem
* Applies identical preprocessing as training
* Runs predictions on inference input data

Outputs are written to:

```
outputs/predictions.json
```

Sample inference data can be generated using:

```bash
python data/inference/generate_sample.py
```



## 🌐 Online Inference API

This branch exposes a **FastAPI-based online inference service** for real-time
housing price predictions.

### API Characteristics

* FastAPI REST service
* Request/response validation using Pydantic
* Artifact loading from `artifacts/production` at startup
* Shared preprocessing logic with training & batch inference
* Structured file-based logging
* Automated API tests
* Dockerized for deployment

### Available Endpoints

* `GET /health` — health check
* `POST /predict` — run housing price predictions



## ▶️ Running the API Locally (Python Environment)

### 1️⃣ Install API dependencies

```bash
pip install -r requirements/api.txt
```

### 2️⃣ Set Python path
```bash
export PYTHONPATH=$(pwd)/src
```

### 3️⃣ Start the API server

```bash
uvicorn api.main:app --reload
```

* API: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)


## 🐳 Running the API with Docker

```bash
docker build -t housing-api .
docker run -p 8000:8000 housing-api
```


## 🧪 Running Tests

```bash
pytest -v
```

## 📌 Note

This branch represents a **filesystem-based API design** and is intentionally
kept as a stable reference point.

The **current production-grade MLOps implementation**, using MLflow for model
registry and lifecycle management, is available in the `main` branch.


---