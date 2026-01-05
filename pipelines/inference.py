"""
Batch inference pipeline
------------------------
- Loads Production model from MLflow
- Loads input data
- Runs predictions
- Saves predictions
"""

import logging
import json
from pathlib import Path
import pandas as pd
import mlflow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("inference_pipeline")


MODEL_URI = "models:/CaliforniaHousingRegressor@Production"   # Alias based
# MODEL_URI = "models:/CaliforniaHousingRegressor/1"            # Version based
# MODEL_URI = "serving/models/"    # Local path based

INPUT_DATA = Path("data/inference/sample_input.csv")
OUTPUT_PATH = Path("outputs/batch_run_001.json")


def run_inference():
    logger.info("Starting batch inference pipeline")

    # --------------------------------------------------
    # Load model from MLflow
    # --------------------------------------------------
    logger.info("Loading Production model from MLflow")
    model = mlflow.pyfunc.load_model(MODEL_URI)

    # --------------------------------------------------
    # Load input data
    # --------------------------------------------------
    logger.info("Loading input data")
    df = pd.read_csv(INPUT_DATA)

    if "median_house_value" in df:
        df = df.drop(columns=["median_house_value"])

    # --------------------------------------------------
    # Run predictions
    # --------------------------------------------------
    logger.info("Running predictions")
    predictions = model.predict(df)

    # --------------------------------------------------
    # Save predictions
    # --------------------------------------------------
    logger.info("Saving predictions")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(
            {"predictions": predictions.tolist()},
            f,
            indent=2,
        )

    logger.info("Batch inference pipeline completed successfully")


if __name__ == "__main__":
    run_inference()
