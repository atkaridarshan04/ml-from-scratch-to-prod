
# MLflow Model Registry & Promotion Strategy

This document describes how models are registered, versioned, and promoted
using the MLflow Model Registry.

The registry acts as the **contract** between training and inference.



## 🎯 Purpose of the Model Registry

The Model Registry is used to:

- Store versioned models
- Track model history
- Enable safe promotion and rollback
- Decouple training from inference deployment



## 📦 Registered Model

All trained models are registered under the name:

```
CaliforniaHousingRegressor
```

Each training run that logs a model creates a **new model version**.



## 🔢 Model Versions

- Each model version corresponds to a specific training run
- Versions are immutable
- Version numbers are assigned by MLflow

A model version encapsulates:
- Preprocessing logic
- Feature engineering logic
- Trained model parameters


## 🏷️ Model Aliases

This project uses **model aliases** to manage deployment state.

The alias:

```
Production
```

always points to the currently approved model version.

During training:
- A new model version is registered
- The `Production` alias is updated to point to the new version

![mlflow-model-version](../__assets/mlflow-model-version.png)

Inference always resolves the model via:

```python
models:/CaliforniaHousingRegressor@Production # Alias based
# or
models:/CaliforniaHousingRegressor/1        # Version based
```



## 🧭 Design Principles

* One model version = one behavior
* Aliases control deployment state
* Inference remains environment-agnostic
* Model lifecycle is centralized and auditable

---