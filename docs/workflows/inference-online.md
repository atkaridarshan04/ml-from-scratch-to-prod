# Online Inference Workflow

## Architecture Overview

Online inference uses **KServe with MLServer runtime** for production-grade model serving with:
- **Direct S3 model loading**: No MLflow runtime dependency
- **V2 protocol only**: Tensor-based inference
- **MLflow PyFunc compatibility**: Preprocessing bundled with model
- **Production scalability**: Kubernetes-native serving

**Critical principle**: Inference pods **never talk to MLflow**. They only read from S3.

## High-Level Flow

1. **KServe** pulls MLflow PyFunc model from **resolved S3 path**
2. **MLServer** loads model with preprocessing bundled
3. **V2 protocol** accepts tensor-based requests
4. **PyFunc model** handles preprocessing + prediction
5. **Predictions** returned in V2 response format

## Request Lifecycle

### Model Loading (Startup)
At InferenceService startup:
- **KServe downloads** model artifacts from physical S3 URI
- **MLServer loads** MLflow PyFunc model
- **Preprocessing logic** is bundled within the model
- **Model signature** enforced for input validation
- **No MLflow service dependency** - purely S3-based loading

### V2 Request Handling
For each `/v2/models/{model}/infer` request:
1. **V2 tensor format** validated by MLServer
2. **MLServer** converts tensors to DataFrame
3. **PyFunc model** applies preprocessing + prediction
4. **Results** returned in V2 tensor format

### Preprocessing Integration
All preprocessing logic is bundled within the model:
- **Imputation**: Handled by bundled transformers
- **Encoding**: Handled by bundled transformers
- **Feature engineering**: Handled by model code
- **Input validation**: Enforced by MLflow signatures


## Model Resolution and Loading

### Deployment-Time Resolution
Logical model references are resolved outside the inference runtime.

```bash
models:/CaliforniaHousingRegressor@production
          ↓
MLflow Model Registry
          ↓
get_model_version_download_uri(name, version)
          ↓
s3://mlflow-artifact-store/.../models/m-<id>/artifacts
```


### KServe Configuration
```yaml
spec:
  predictor:
    model:
      storageUri: "s3://mlflow-artifact-store/.../models/m-<id>/artifacts"
```

### Runtime Loading Process
- **KServe** downloads artifacts from S3 `storageUri`
- **MLServer** loads complete MLflow PyFunc model
- **No registry lookup** - uses cached S3 artifacts
- **Self-contained** - all code and dependencies included

## V2 Protocol Details

### Endpoint Format
```
POST /v2/models/{model_name}/infer
```

### Request Format (Tensor-based)
```json
{
  "inputs": [
    {
      "name": "longitude",
      "shape": [2],
      "datatype": "FP64",
      "data": [-122.23, -122.22]
    },
    {
      "name": "latitude", 
      "shape": [2],
      "datatype": "FP64",
      "data": [37.88, 37.86]
    }
  ]
}
```

**Important**: V1 endpoints (`/v1/models/{model}:predict`) are **not available** with MLServer runtime.

---