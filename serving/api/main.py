import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes import router as prediction_router
import mlflow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("api")

MODEL_URI = "models/"

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info("Loading Model from MLFlow")

    # Store the model to app state
    app.state.model = mlflow.pyfunc.load_model(MODEL_URI)
    logger.info("Model loaded successfully")
    
    yield
    logger.info("API shutdown")


app = FastAPI(
    title="California Housing Price Prediction API",
    description="Online inference API for housing price prediction",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(prediction_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}