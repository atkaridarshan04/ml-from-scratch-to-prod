# Training Pipeline

## Purpose

The training pipeline is responsible for:
- Training the model
- Evaluating performance
- Registering a Production-ready model

## Key steps

1. Load raw dataset
2. Split into train/test
3. Apply preprocessing & feature engineering
4. Train model
5. Evaluate metrics
6. Log everything to MLflow
7. Register model & update alias

## Output

- MLflow experiment run
- Registered model version
- Updated `Production` alias
