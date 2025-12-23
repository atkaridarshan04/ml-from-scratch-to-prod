"""
Training pipeline
----------------------------------------------------------
- Loads raw data
- Applies preprocessing & feature engineering
- Trains HistGradientBoostingRegressor
- Evaluates on holdout set
- Saves model, preprocessors, and metrics
"""

import pandas as pd
from pathlib import Path

from preprocessing import (
    split_features,
    train_test_split_data,
    fit_median_imputer,
    apply_imputer_transformation,
    fit_one_hot_encoder,
    apply_one_hot_encoder,
    add_engineered_features,
)

from models import fit_hgb_model, evaluate_regression
from inference import predict
from utils import save_joblib, save_json, get_logger

LOG_DIR = Path("logs")
logger = get_logger(
    name="train_pipeline",
    log_file=LOG_DIR / "train.log"
)

ARTIFACT_DIR = Path("artifacts/production")
DATA_PATH = Path("data/raw/housing.csv")
TARGET_COL = "median_house_value"


def run_training():
    logger.info("Starting training pipeline")
    # --------------------------------------------------
    # Load data
    # --------------------------------------------------
    logger.info("Loading raw dataset")
    df = pd.read_csv(DATA_PATH)

    # --------------------------------------------------
    # Split features & target
    # --------------------------------------------------
    logger.info("Splitting features and target")
    X, y = split_features(df, TARGET_COL)
    X_train, X_test, y_train, y_test = train_test_split_data(
        X, y, test_size=0.2, random_state=42
    )

    # --------------------------------------------------
    # Imputation
    # --------------------------------------------------
    logger.info("Fitting and applying imputer")
    column_to_impute = "total_bedrooms"
    imputer = fit_median_imputer(X_train, column_to_impute)   # (fit on train only)

    X_train = apply_imputer_transformation(X_train, column_to_impute, imputer)
    X_test = apply_imputer_transformation(X_test, column_to_impute, imputer)

    # --------------------------------------------------
    # Encoding 
    # --------------------------------------------------
    logger.info("Fitting and applying one-hot encoder")
    column_to_encode = "ocean_proximity"
    encoder = fit_one_hot_encoder(X_train, column_to_encode)   # (fit on train only)

    X_train = apply_one_hot_encoder(X_train, column_to_encode, encoder)
    X_test = apply_one_hot_encoder(X_test, column_to_encode, encoder)

    # --------------------------------------------------
    # Feature engineering
    # --------------------------------------------------
    logger.info("Applying feature engineering")
    X_train = add_engineered_features(X_train)
    X_test = add_engineered_features(X_test)

    # --------------------------------------------------
    # Train model
    # --------------------------------------------------
    logger.info("Training HistGradientBoostingRegressor")
    params = {
        "max_depth": 8,
        "learning_rate": 0.1,
        "max_iter": 200,
        "random_state": 42
    }

    model = fit_hgb_model(X_train, y_train, params)

    # --------------------------------------------------
    # Evaluate
    # --------------------------------------------------
    logger.info("Evaluating model")
    y_train_pred = predict(model, X_train)
    y_test_pred = predict(model, X_test)

    train_metrics = evaluate_regression(y_train, y_train_pred)
    test_metrics = evaluate_regression(y_test, y_test_pred)

    logger.info(f"Train metrics: {train_metrics}")
    logger.info(f"Test metrics : {test_metrics}")

    # --------------------------------------------------
    # Prepare metrics structure
    # --------------------------------------------------
    metrics = {
        "model_family": "gradient_boosting",
        "model_name": "hist_gradient_boosting",
        "holdout": {
            "train": train_metrics,
            "test": test_metrics
        }
    }

    # --------------------------------------------------
    # Save artifacts
    # --------------------------------------------------
    logger.info("Saving model and artifacts")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    save_joblib(model, ARTIFACT_DIR / "model.joblib")
    save_joblib(imputer, ARTIFACT_DIR / "imputer.joblib")
    save_joblib(encoder, ARTIFACT_DIR / "encoder.joblib")
    save_json(metrics, ARTIFACT_DIR / "metrics.json")

    logger.info("Training pipeline completed successfully")


if __name__ == "__main__":
    run_training()
