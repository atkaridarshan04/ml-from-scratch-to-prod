"""
Training pipeline
----------------------------------------------------------
- Loads raw data
- Applies preprocessing & feature engineering
- Trains HistGradientBoostingRegressor (approved Production model)
- Evaluates on holdout set
- Logs params, metrics, dataset lineage, preprocessors, and model to MLflow
- Registers model and assigns a Production alias (modern MLflow practice)
"""

import logging
import pandas as pd
from pathlib import Path
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import yaml
from inference import HousingInferencePipeline
import mlflow.pyfunc
from mlflow.models import infer_signature

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


# --------------------------------------------------
# Config
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("train_pipeline")


DATA_PATH = Path("data/raw/housing.csv")
DVC_FILE = Path("data/raw/housing.csv.dvc")
TARGET_COL = "median_house_value"

EXPERIMENT_NAME = "california_housing_price"
RUN_NAME = "hist_gradient_boosting"

REGISTERED_MODEL_NAME = "CaliforniaHousingRegressor"
MODEL_ALIAS = "Production" 


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def get_dvc_data_md5() -> str:
    """Read dataset hash directly from .dvc file"""
    try:
        with open(DVC_FILE) as f:
            dvc_yaml = yaml.safe_load(f)
        return dvc_yaml["outs"][0]["md5"]
    except Exception:
        return "unknown"


# --------------------------------------------------
# Training Pipeline
# --------------------------------------------------
def run_training():
    logger.info("Starting training pipeline")

    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(run_name=RUN_NAME) as run:
        logger.info(f"MLflow run started with run_id={run.info.run_id}")

        # --------------------------------------------------
        # Load data
        # --------------------------------------------------
        logger.info("Loading raw dataset")
        df = pd.read_csv(DATA_PATH)

        dataset = mlflow.data.from_pandas(
            df,
            name="california_housing_raw",
        )
        mlflow.log_input(dataset, context="training")
        mlflow.set_tag("data_dvc_md5", get_dvc_data_md5())

        # --------------------------------------------------
        # Train / test split
        # --------------------------------------------------
        X, y = split_features(df, TARGET_COL)
        X_raw_train, X_raw_test, y_train, y_test = train_test_split_data(
            X, y, test_size=0.2, random_state=42
        )
        logger.info("Train Test Split Completed")

        # --------------------------------------------------
        # Imputation
        # --------------------------------------------------
        imputer = fit_median_imputer(X_raw_train, "total_bedrooms")
        X_train = apply_imputer_transformation(X_raw_train, "total_bedrooms", imputer)
        X_test = apply_imputer_transformation(X_raw_test, "total_bedrooms", imputer)
        logger.info("Imputation Completed")

        # --------------------------------------------------
        # Encoding
        # --------------------------------------------------
        encoder = fit_one_hot_encoder(X_train, "ocean_proximity")
        X_train = apply_one_hot_encoder(X_train, "ocean_proximity", encoder)
        X_test = apply_one_hot_encoder(X_test, "ocean_proximity", encoder)
        logger.info("Encoding Completed")

        # --------------------------------------------------
        # Feature engineering
        # --------------------------------------------------
        X_train = add_engineered_features(X_train)
        X_test = add_engineered_features(X_test)
        logger.info("Feature Engineering Completed")

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
        logger.info("Model Trainning Finished")

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

        logger.info("Metrics Evaluation Completed")

        # --------------------------------------------------
        # Build inference pipeline (preprocessing + model)
        # --------------------------------------------------
        inference_pipeline = HousingInferencePipeline(
            imputer=imputer,
            encoder=encoder,
            model=model,
        )
        logger.info("Unifined Model is ready")

        # --------------------------------------------------
        # Log and register unified model with signature
        # --------------------------------------------------

        input_example = X_raw_train.iloc[:3].copy()
        pred_example = inference_pipeline.predict(input_example)
        signature = infer_signature(input_example, pred_example)

        mlflow.pyfunc.log_model(
            name="model",
            python_model=inference_pipeline,
            # code_paths=["src"],       # if custom code is needed
            pip_requirements="requirements/train.txt",
            registered_model_name=REGISTERED_MODEL_NAME,
            input_example=input_example,
            signature=signature,
        )
        logger.info("Unified model looged and registered sucessfully")

        # --------------------------------------------------
        # Log the hgb model
        # --------------------------------------------------
        # mlflow.sklearn.log_model(
        #     sk_model=model,
        #     name="hgb-model",
        # )

        # --------------------------------------------------
        # Assign model alias
        # --------------------------------------------------
        client = MlflowClient()
        model_versions = client.search_model_versions(
            f"name='{REGISTERED_MODEL_NAME}'"
        )

        # Find model version created by this run
        current_version = next(
            mv.version for mv in model_versions if mv.run_id == run.info.run_id
        )

        # Set alias to point to current version
        client.set_registered_model_alias(
            name=REGISTERED_MODEL_NAME,
            alias=MODEL_ALIAS,
            version=current_version,
        )

        logger.info(
            f"Model version {current_version} promoted via alias '{MODEL_ALIAS}'"
        )

        # --------------------------------------------------
        # Cleanup temporary artifact directory
        # --------------------------------------------------
        # shutil.rmtree(ARTIFACT_DIR, ignore_errors=True)

        logger.info("Training pipeline completed successfully")


if __name__ == "__main__":
    run_training()
