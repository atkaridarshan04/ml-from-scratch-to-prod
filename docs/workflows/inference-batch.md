# Batch Inference Pipeline

## Purpose

Batch inference is used for offline prediction use cases where
real-time responses are not required.

## Behavior

- **Loads MLflow PyFunc model** from registry using `production` alias
- **Accepts raw input data** (same format as training data)
- **Applies bundled preprocessing** automatically within the model
- **Runs predictions** using the unified model artifact
- **Writes results** to disk `outputs/batch_run_001.json`

## MLflow PyFunc Integration

Batch inference uses the same unified model as KServe online inference:

```python
model = mlflow.pyfunc.load_model("models:/CaliforniaHousingRegressor@production")
predictions = model.predict(context=None, model_input=raw_data)
```

## Key Design Choice

Batch inference uses the same model artifacts as online inference, ensuring consistent behavior.
