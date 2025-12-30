import logging
import pandas as pd
from fastapi import APIRouter, HTTPException, Request

from api.schemas import PredictionRequest, PredictionResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("api-predict")

router = APIRouter()

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Run housing price predictions",
)
def predict_prices(
    request: PredictionRequest, http_request: Request
):
    """
    Run model inference on input housing features.
    """
    try:
        # Convert request data to DataFrame
        records = [row.model_dump() for row in request.data]
        df = pd.DataFrame(records)

        logger.info(f"Received prediction request with {len(df)} records")

        # Import the unified model from app state
        model = http_request.app.state.model 
        preds = model.predict(df)

        logger.info("Prediction request completed successfully")

        return PredictionResponse(predictions=preds.tolist())


    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))
