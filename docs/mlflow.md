# MLflow Architecture & Usage

This document describes how **MLflow is deployed, used, and integrated** within the platform, including experiment tracking, model registry, artifact storage, and its interaction with Kubernetes, DVC, and KServe.

MLflow acts strictly as the **control plane** for metadata, governance, and lineage.
It is **not** used at inference runtime.



## 1. MLflow Deployment Architecture

### In-Cluster MLflow

MLflow runs **inside the Kubernetes cluster** with the following configuration:

- **Deployment model**: Kubernetes Deployment
- **Image**: Custom-built MLflow image
- **Backend store**: In-cluster PostgreSQL (temporary)
- **Artifact store**: Amazon S3
- **Service endpoint**:

  ```bash
  MLFLOW_TRACKING_URI=http://mlflow.mlflow.svc.cluster.local:5000
  ```

This setup allows all in-cluster workloads (training jobs, promotion scripts) to interact with MLflow without external dependencies.

---

### Why a Custom MLflow Image

The official MLflow images are intentionally minimal and unsuitable for production use when external services are involved.

Production requirements include:

* **boto3 / botocore**
  Required for S3-based artifact storage
* **psycopg2**
  Required for PostgreSQL backend store connectivity

Because of this, a **custom MLflow image is built and maintained** with all required dependencies preinstalled.

---

### Current vs Future State

| Component     | Current State          | Future State             |
| ------------- | ---------------------- | ------------------------ |
| Backend DB    | In-cluster PostgreSQL  | Amazon RDS               |
| Artifact Auth | Static AWS credentials | IRSA / workload identity |
| Access        | Cluster-local          | Ingress + auth           |


## 2. MLflow Experiment Tracking

### Purpose and Role

MLflow serves as the **control plane for ML metadata**, enabling:

* Experiment comparison
* Performance tracking over time
* Reproducibility
* Lineage across code, data, and models

**Important**:
MLflow UI and APIs are **not used by inference runtimes**.

---

### Experiment Structure

All training runs are logged under a single experiment:

```
california_housing_price
```

Each Kubernetes training job execution maps to **one MLflow run**.

---

### What Gets Logged Per Run

#### Parameters and Configuration

* Model hyperparameters:

  * `max_depth`
  * `learning_rate`
  * `max_iter`
  * `random_state`
* Training configuration
* Random seeds

---

#### Metrics and Performance

* Training metrics (RMSE, R²)
* Validation/test metrics (RMSE, R²)
* Metrics logged independently for comparison

---

#### Dataset Lineage

* Dataset logged via **MLflow dataset tracking**
* **DVC dataset hash** stored as MLflow tag
* **S3 data path** recorded

This guarantees each model can be traced back to the **exact dataset version** used.

![mlflow-experiments](./__assets/mlflow-experiment.png)

---

### Source Code Preservation (Critical)

To prevent training–serving skew, all inference-related code is packaged with the model:

* Entire `src/` directory included using `code_paths`
* Preprocessing and feature engineering preserved
* Absolute imports enforced

This ensures:

* Identical code in training and inference
* Self-contained model artifacts

---

### Artifacts

Each run logs:

* Unified PyFunc model
* MLflow metadata and signatures
* Bundled source code
* Environment specifications

![mlflow-artifacts](./__assets/mlflow-artifacts.png)



## 3. Model Registry & Artifact Storage

### Architecture Overview

The system enforces a strict separation of concerns:

* **MLflow Model Registry**
  Versioning, aliases, governance
* **Amazon S3**
  Immutable model artifacts
* **KServe**
  Online inference and serving

Inference runtimes **never talk to MLflow directly**.

---

### Registered Model

All trained models are registered under a single logical name:

```
CaliforniaHousingRegressor
```

![mlflow-amodel-version](./__assets/mlflow-model-version.png)

---

### Model Aliases

The `production` alias represents the **currently approved model version**.

Training flow:

1. Training job logs a new model version
2. Artifacts are stored in S3
3. Alias update is performed **manually** (for now)

> Alias updates are intentionally decoupled from training to allow human or automated approval workflows later.

---

### Resolution Flow (Critical)

Aliases and registry URIs are **logical references only**.
KServe requires a **physical object storage path**.

The **exact resolution logic** is:

#### 1) Logical reference
```text
models:/CaliforniaHousingRegressor@production
```

#### 2) Resolve to artifact URI
```python
mv = client.get_model_version_by_alias("CaliforniaHousingRegressor", "production")
uri = client.get_model_version_download_uri("CaliforniaHousingRegressor", mv.version)
```

#### 3) Physical artifact path
```text
s3://mlflow-artifact-store/.../models/m-<id>/artifacts
```

#### 4) KServe (InferenceService)
```yaml
storageUri: s3://mlflow-artifact-store/.../models/m-<id>/artifacts
```

A helper script is provided to perform this resolution:

```
scripts/resolve_model_artifact_uri.py
```

---

### Usage Patterns

#### Batch Inference

Batch jobs may directly use MLflow registry references:

```python
model = mlflow.pyfunc.load_model(
    "models:/CaliforniaHousingRegressor@production"
)
```

MLflow resolves the registry indirection internally.

---

#### Online Inference (KServe)

KServe must be configured with **resolved S3 paths**:

```yaml
spec:
  predictor:
    model:
      storageUri: s3://mlflow-artifact-store-123-da/1/models/m-7065bfbb8b9f436fb9eafdcb97e192a9/artifacts/
```


## 4. Access Patterns

### Training Jobs (In-Cluster)

```bash
MLFLOW_TRACKING_URI=http://mlflow.mlflow.svc.cluster.local:5000
```

Used by Kubernetes training jobs and promotion utilities.

---

### MLflow UI

```bash
http://localhost:5000
```

Accessed via port-forwarding during development.

> Ingress, authentication, can be added in future iterations.

---
