# 🧪 Local Development Environment

This document describes how to run the project **locally (without Docker)** for
development and debugging.

It covers:
- Running MLflow locally
- Executing the training pipeline
- Running batch inference
- Running the online inference API



## 🧠 Local Execution Model

In local mode:

- Training pipelines run as Python processes on the host
- MLflow runs as a local tracking server
- Batch and online inference load models from MLflow
- No model artifacts are loaded from local files

MLflow acts as the integration point between training and inference.



## 📈 Running MLflow Locally

### Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install API dependencies

```bash
pip install --upgrade pip
pip install -r requirements/train.txt
```


### ▶️ Start MLflow Tracking Server

From the project root:

```bash
mlflow server \
  --host 127.0.0.1 \
  --port 5000 \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root "$(pwd)/mlruns"
````

MLflow UI will be available at:

```
http://localhost:5000
```


## 🌍 Required Environment Variables

Before running any training or inference code:

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
export PYTHONPATH=$(pwd)/src
```

> MLflow automatically reads `MLFLOW_TRACKING_URI` from the environment.
> The tracking URI is not set in application code.



## 🏋️ Training Pipeline (Local)

### ▶️ Run training

```bash
python -m pipelines.train
```

### What this command does

* Executes the training pipeline locally
* Logs parameters, metrics, and artifacts to MLflow
* Registers a new model version in the MLflow Model Registry
* Updates the `Production` alias

Each execution corresponds to a single MLflow run.

### Download the trained model form MLflow

```bash
mlflow artifacts download -u models:/CaliforniaHousingRegressor@Production -d ./serving/models
```

<!-- Detailed training logic and model lifecycle behavior are documented in:

```
docs/workflows/training.md
docs/mlflow/model-registry.md
``` -->



## 📦 Batch (Offline) Inference

Batch inference is used for offline predictions on CSV inputs.

### ▶️ Run batch inference

```bash
python -m pipelines.inference
```

### What this command does

* Loads the `Production` model from MLflow
* Accepts raw input data
* Runs predictions
* Writes results to disk

### Output location

```
outputs/batch_run_001.json
```

### Generate sample input data

```bash
python data/inference/generate_sample.py
```

Detailed batch inference behavior is documented in: [docs/workflows/inference-batch.md](../workflows/inference-batch.md)


## ▶️ Run the Online Inference API locally


#### 1️⃣ Install API dependencies

```bash
pip install -r requirements/api.txt
```

#### 2️⃣ Start the API server


```bash
cd serving  
uvicorn api.main:app --reload
```



### Access the API

* Health Check: [http://localhost:8000/health](http://localhost:8000/health)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

* Predict Endpoint: [http://localhost:8000/predict](http://localhost:8000/predict)
Executing a POST request to this endpoint with input data will return predictions.

  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/predict' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "data": [
      {
        "households": 126,
        "housing_median_age": 41,
        "latitude": 37.88,
        "longitude": -122.23,
        "median_income": 8.3252,
        "ocean_proximity": "NEAR BAY",
        "population": 322,
        "total_bedrooms": 129,
        "total_rooms": 880
      }
    ]
  }'
  ```


## 🧪 API Tests

```bash
pytest -v
```

---

