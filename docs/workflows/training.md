# Training Pipeline

## Architecture Overview

Training runs as **ephemeral Kubernetes Jobs** that pull code and data at runtime, execute training, and persist all outputs to MLflow/S3 before terminating.

**Key components**:
- **Custom trainer image**: Python 3.10 with MLflow, DVC, scikit-learn
- **Runtime code**: Repository cloned during job execution
- **Data access**: `dvc pull` retrieves datasets from S3
- **Output persistence**: MLflow experiments + S3 artifacts

## Training Workflow

### Job Execution Flow
1. **Clone repository** to get latest training code
2. **DVC pull** retrieves exact dataset version from S3
3. **Execute training** via `pipelines/train.py`
4. **Log to MLflow** (tracking URI: `http://mlflow.mlflow.svc.cluster.local:5000`)
5. **Register model** 
6. **Job terminates**

### Data Pipeline
- **DVC pull** retrieves exact dataset version from S3
- **Dataset logged** to MLflow for lineage tracking
- **Deterministic split** into train/test with fixed random state

### Model Pipeline
- **Preprocessing fitted** on training data (imputation, encoding)
- **Model trained** with logged hyperparameters
- **Evaluation** on both training and test sets
- **Unified PyFunc** packages preprocessing + model + code

## MLflow Integration

The training pipeline creates a unified model artifact:

```python
inference_pipeline = HousingInferencePipeline(
    imputer=imputer,
    encoder=encoder, 
    model=model,
)

mlflow.pyfunc.log_model(
    python_model=inference_pipeline,
    code_paths=["src"],  # Bundle source code
    signature=signature,  # Enforce input/output schema
    registered_model_name="CaliforniaHousingRegressor"
)
```

## Environment Configuration

### Kubernetes Job Environment
- **Python 3.10**: Matches serving environment to avoid serialization issues
- **MLflow URI**: `http://mlflow.mlflow.svc.cluster.local:5000`
- **S3 credentials**: Static credentials (IRSA deferred to future)
- **Dependencies**: Captured in custom trainer image

### Output Artifacts
- **MLflow experiment run**: Parameters, metrics, dataset lineage
- **S3 model artifacts**: PyFunc model + code + dependencies
- **Model Registry**: New version

---