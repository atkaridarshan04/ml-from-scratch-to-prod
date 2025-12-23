import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException

from api.schemas import PredictionRequest, PredictionResponse
from inference import preprocess_input, predict
from utils import get_logger

LOG_DIR = Path("logs")
logger = get_logger(
    name="api.predict",
    log_file=LOG_DIR / "api.log"
)

router = APIRouter()

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Run housing price predictions",
)
def predict_prices(
    request: PredictionRequest,
):
    """
    Run model inference on input housing features.
    """
    try:
        # Convert request data to DataFrame
        records = [row.model_dump() for row in request.data]
        df = pd.DataFrame(records)

        logger.info(f"Received prediction request with {len(df)} records")

        # Load artifacts from app state
        from api.main import ARTIFACTS

        if not ARTIFACTS:
            raise RuntimeError("Model artifacts not loaded")

        # Preprocess
        X = preprocess_input(df, ARTIFACTS)

        # Predict
        preds = predict(ARTIFACTS["model"], X)
        logger.info("Prediction request completed successfully")

        return PredictionResponse(predictions=preds.tolist())


    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))
