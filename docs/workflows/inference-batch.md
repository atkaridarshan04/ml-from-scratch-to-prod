# Batch Inference Pipeline

## Purpose

Batch inference is used for offline prediction use cases where
real-time responses are not required.

## Behavior

- Loads the `Production` model from MLflow
- Accepts raw input data
- Runs predictions
- Writes results to disk `outputs/batch_run_001.json`

## Key design choice

Batch inference uses the same model artifact as online inference,
ensuring consistent behavior.
