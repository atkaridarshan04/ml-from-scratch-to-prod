# 🚀 ML from Scratch to Production

<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Scikit Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![DVC](https://img.shields.io/badge/DVC-13ADC7?logo=dvc&logoColor=white)](https://dvc.org/)
[![MLflow](https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white)](https://mlflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An end-to-end Machine Learning engineering project that demonstrates how an ML system evolves from experimentation into a production-ready, containerized, and deployable service.**

</div>



## 🎯 Project Overview

This repository demonstrates the **full lifecycle of a Machine Learning system**, from early experimentation to production-oriented deployment.

Using the **California Housing dataset**, the project focuses on **engineering practices**:

- Reproducible training pipelines
- Explicit separation between training and serving
- Model lifecycle management with MLflow
- Batch and online inference workflows
- Docker-first execution
- Kubernetes-ready architecture



## 🌿 Branch Architecture

This repository is structured as a **progressive learning path**, with each branch representing a stage in ML system maturity.

| Branch | Focus | Key Question |
|------|------|-------------|
| `ml-baseline` | ML experimentation | *How do we explore data and choose a model?* |
| `api-baseline` | Serving fundamentals | *How do we expose a trained model?* |
| `main` | Production MLOps | *How does this become reliable and deployable?* |

The `main` branch represents the **final, production-oriented design**.



## 🏗️ System Architecture Overview

```mermaid
graph TB
    subgraph "Data Layer"
        A[Raw Data<br/>data/raw/housing.csv] --> B[DVC Versioning]
    end
    
    subgraph "Training Pipeline"
        C[Training Script<br/>pipelines/train.py] --> D[MLflow Tracking]
        D --> E[Model Registry<br/>CaliforniaHousingRegressor]
    end
    
    subgraph "Inference Layer"
        F[Batch Inference<br/>pipelines/inference.py]
        G[Online API<br/>src/api/]
        E --> F
        E --> G
    end
    
    subgraph "Deployment"
        H[Docker Compose]
        I[Kubernetes/KServe]
        G --> H
        G --> I
    end
    
    A --> C
    B --> C
```



## 🚀 Quick Start (Main Branch)

```bash
git clone https://github.com/atkaridarshan04/ml-from-scratch-to-prod.git
cd ml-from-scratch-to-prod
git checkout main
```

### Local Development 

➡️ See: [docs/environments/local.md](./docs/environments/local.md)



## 🗂️ Project Structure (Main)

```
ml-from-scratch-to-prod/
├── .dvc/                 # DVC configuration
├── data/                 # Raw data and inference inputs
├── docs/                 # Architecture, workflows, and decisions
├── pipelines/            # Training & batch inference entry points
├── serving               # Serving layer (API code & model artifacts)
├── src/                  # Core ML logic
├── tests/                # API tests
├── requirements/         # Dependency separation (train / api)
├── Dockerfile            # Docker image for api serving
└── README.md             # This file
```



## 📚 Documentation Hub

All documentation lives under `docs/` and is organized by **concern**.

| Area            | Description                                   |
| --------------- | --------------------------------------------- |        
| [codebase/](./docs/codebase/)     | Source code organization and design decisions |
| [workflows/](./docs/workflows/)    | Training and inference pipelines              |
| [environments/](./docs/environments/) | Local, Docker, and Kubernetes execution       |
| [mlflow/](./docs/mlflow/)       | Experiment tracking and model lifecycle       |        

Start here:

➡️ [docs/README.md](./docs/README.md)



## 🧪 Testing

```bash
pytest -v
```

## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

---