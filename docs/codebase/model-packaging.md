# Model Packaging Strategy (MLflow PyFunc with Unified Preprocessing)

This document explains how and why the project packages preprocessing,
feature engineering, and the trained model into a **single unified MLflow PyFunc model**.

## 🎯 Problem

During early iterations of this project, inference was implemented by
loading and applying multiple independent artifacts, including:

- The trained model
- A fitted imputer
- A fitted encoder
- Feature engineering logic executed in application code

While this approach worked functionally, it introduced several issues
as the system evolved toward a production-style setup.

Specifically, we observed the following risks:

- **Training–serving skew**, where preprocessing logic in the API could
  diverge from the logic used during training
- **Version mismatches** between preprocessing artifacts and the trained
  model when retraining or rolling back models
- **Tight coupling** between inference code and preprocessing
  implementation details, making the API harder to maintain and test


## ✅ Design Decision: MLflow PyFunc with Bundled Preprocessing

We package **all inference-time logic** into a **single MLflow PyFunc model artifact**, which is then registered and versioned in MLflow. 

### Why MLflow PyFunc?

MLflow PyFunc provides:
- **Custom model classes** that can encapsulate preprocessing + prediction
- **Code packaging** via `code_paths=["src"]` for absolute imports
- **Environment consistency** through conda/pip requirements
- **Signature enforcement** for input/output validation
- **KServe compatibility** via MLServer runtime

### PyFunc Predict Contract

The model uses the canonical PyFunc signature required for MLServer compatibility:

```python
def predict(self, context, model_input, params=None):
    # Preprocessing + prediction logic
    return predictions
```

This signature is **mandatory** for KServe V2 protocol support.


## 🏗️ Implementation: HousingInferencePipeline

The unified model is implemented as:

```python
class HousingInferencePipeline(mlflow.pyfunc.PythonModel):
    def __init__(self, imputer, encoder, model):
        self.imputer = imputer
        self.encoder = encoder  
        self.model = model
    
    def predict(self, context, model_input: pd.DataFrame, params=None):
        X = self.preprocess(model_input)
        return self.model.predict(X)
```

See [src/inference/pipeline.py](../../src/inference/pipeline.py) for full implementation.


## 📦 Code Packaging Rules

### Absolute Imports with src/ Package

All inference code uses **absolute imports**:

```python
from src.preprocessing.imputation import apply_imputer_transformation
from src.preprocessing.encoding import apply_one_hot_encoder
```

### Code Paths Configuration

Models are logged with:

```python
mlflow.pyfunc.log_model(
    python_model=inference_pipeline,
    code_paths=["src"],  # Packages entire src/ directory
    # ...
)
```

A single model version represents:
- Exact preprocessing steps (fitted transformers)
- Exact feature engineering logic
- Exact trained model parameters
- Exact code dependencies

## Inference Interface

Inference consumes **one object** and calls:

```python
model.predict(context, raw_input_df)
```

No preprocessing logic exists outside the model artifact.

---