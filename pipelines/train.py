"""
Training pipeline
----------------------------------------------------------
- Loads raw data (via DATA_URI)
- Applies preprocessing & feature engineering
- Trains HistGradientBoostingRegressor
- Evaluates on holdout set
- Logs params, metrics, dataset lineage, preprocessors, and model to MLflow
- Registers model version in MLflow (NO promotion / deployment decision)
"""

import os
import logging
import yaml
import pandas as pd
import mlflow
import mlflow.pyfunc
from mlflow.models import infer_signature

from src.inference.pipeline import HousingInferencePipeline
from src.preprocessing import (
    split_features,
    train_test_split_data,
    fit_median_imputer,
    apply_imputer_transformation,
    fit_one_hot_encoder,
    apply_one_hot_encoder,
    add_engineered_features,
)
from src.models import fit_hgb_model, evaluate_regression


# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("train_pipeline")


# --------------------------------------------------
# Runtime configuration (injected)
# --------------------------------------------------
DATA_URI = os.environ.get("DATA_URI")
DVC_FILE = os.environ.get("DVC_FILE", "data/raw/housing.csv.dvc")

if not DATA_URI:
    raise ValueError("DATA_URI environment variable must be set")

TARGET_COL = "median_house_value"

EXPERIMENT_NAME = "california_housing_price"
RUN_NAME = "hist_gradient_boosting"
REGISTERED_MODEL_NAME = "CaliforniaHousingRegressor"


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def get_dvc_md5(dvc_file: str) -> str:
    """
    Extract MD5 hash from a DVC .dvc file.
    This is the authoritative data version used for training.
    """
    try:
        with open(dvc_file) as f:
            dvc_yaml = yaml.safe_load(f)
        return dvc_yaml["outs"][0]["md5"]
    except Exception:
        logger.warning("Unable to read DVC md5 from %s", dvc_file)
        return "unknown"


# --------------------------------------------------
# Training Pipeline
# --------------------------------------------------
def run_training():
    logger.info("Starting training pipeline")
    logger.info("DATA_URI=%s", DATA_URI)
    logger.info("DVC_FILE=%s", DVC_FILE)

    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(run_name=RUN_NAME) as run:
        logger.info("MLflow run started (run_id=%s)", run.info.run_id)

        # --------------------------------------------------
        # Load data
        # --------------------------------------------------
        logger.info("Loading dataset")
        df = pd.read_csv(DATA_URI)

        dataset = mlflow.data.from_pandas(
            df,
            name="california_housing_raw",
        )

        dvc_md5 = get_dvc_md5(DVC_FILE)

        mlflow.log_input(dataset, context="training")
        mlflow.set_tag("data_uri", DATA_URI)
        mlflow.set_tag("data_dvc_md5", dvc_md5)
        # mlflow.set_tag("training_entrypoint", "pipelines.train")

        # --------------------------------------------------
        # Train / test split
        # --------------------------------------------------
        X, y = split_features(df, TARGET_COL)
        X_raw_train, X_raw_test, y_train, y_test = train_test_split_data(
            X, y, test_size=0.2, random_state=42
        )
        logger.info("Train-test split completed")

        # --------------------------------------------------
        # Imputation
        # --------------------------------------------------
        imputer = fit_median_imputer(X_raw_train, "total_bedrooms")
        X_train = apply_imputer_transformation(X_raw_train, "total_bedrooms", imputer)
        X_test = apply_imputer_transformation(X_raw_test, "total_bedrooms", imputer)
        logger.info("Imputation completed")

        # --------------------------------------------------
        # Encoding
        # --------------------------------------------------
        encoder = fit_one_hot_encoder(X_train, "ocean_proximity")
        X_train = apply_one_hot_encoder(X_train, "ocean_proximity", encoder)
        X_test = apply_one_hot_encoder(X_test, "ocean_proximity", encoder)
        logger.info("Encoding completed")

        # --------------------------------------------------
        # Feature engineering
        # --------------------------------------------------
        X_train = add_engineered_features(X_train)
        X_test = add_engineered_features(X_test)
        logger.info("Feature engineering completed")

        # --------------------------------------------------
        # Train model
        # --------------------------------------------------
        params = {
            "max_depth": 8,
            "learning_rate": 0.1,
            "max_iter": 200,
            "random_state": 42,
        }
        mlflow.log_params(params)

        model = fit_hgb_model(X_train, y_train, params)
        logger.info("Model training completed")

        # --------------------------------------------------
        # Evaluate
        # --------------------------------------------------
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        train_metrics = evaluate_regression(y_train, y_train_pred)
        test_metrics = evaluate_regression(y_test, y_test_pred)

        for k, v in train_metrics.items():
            mlflow.log_metric(f"train_{k}", v)
        for k, v in test_metrics.items():
            mlflow.log_metric(f"test_{k}", v)

        logger.info("Evaluation metrics logged")

        # --------------------------------------------------
        # Build unified inference pipeline
        # --------------------------------------------------
        inference_pipeline = HousingInferencePipeline(
            imputer=imputer,
            encoder=encoder,
            model=model,
        )
        logger.info("Unified inference pipeline created")

        # --------------------------------------------------
        # Log and register PyFunc model
        # --------------------------------------------------
        input_example = X_raw_train.iloc[:3].copy()
        pred_example = inference_pipeline.predict(None, input_example)
        signature = infer_signature(input_example, pred_example)

        mlflow.pyfunc.log_model(
            name="model",
            python_model=inference_pipeline,
            code_paths=["src"],
            pip_requirements="requirements.txt",
            registered_model_name=REGISTERED_MODEL_NAME,
            input_example=input_example,
            signature=signature,
        )

        logger.info(
            "Model registered under name '%s' (run_id=%s)",
            REGISTERED_MODEL_NAME,
            run.info.run_id,
        )

        logger.info("Training pipeline completed successfully")


if __name__ == "__main__":
    run_training()
