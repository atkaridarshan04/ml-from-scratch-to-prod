"""
Batch inference pipeline
------------------------
- Loads production artifacts
- Loads input data
- Applies preprocessing
- Runs predictions
- Saves predictions
"""

from inference import load_prod_artifacts, preprocess_input, predict
from utils import get_logger, save_json
from pathlib import Path
import pandas as pd

LOG_DIR = Path('logs')
logger = get_logger(
    name='inference_pipeline',
    log_file=LOG_DIR / 'inference.log'
)

ARTIFACTS_DIR = Path('artifacts/production')
INPUT_DATA = Path('data/inference/sample_input.csv')
OUTPUT_PATH = Path("outputs/batch_run_001.json")

def run_inference():
    logger.info("Starting batch inference pipeline")

    # Load Artifacts
    logger.info("Loading production artifacts")
    artifacts = load_prod_artifacts(ARTIFACTS_DIR)

    # Load Input Data
    logger.info("Loading input data")
    df = pd.read_csv(INPUT_DATA)
    
    # Drop Target if exists
    if "median_house_value" in df:
        df = df.drop(columns=["median_house_value"])

    # Preprocess Input Data
    logger.info("Applying preprocessing")
    X = preprocess_input(df, artifacts)

    # Find Predictions
    logger.info("Running Predictions")
    predictions = predict(artifacts['model'], X)

    # Save predictions
    logger.info("Saving predictions")
    save_json(
        {"predictions": predictions.tolist()},
        OUTPUT_PATH
    )

    logger.info("Inference pipeline completed successfully")

if __name__ == "__main__":
    run_inference()
