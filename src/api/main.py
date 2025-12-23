from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path

from inference.load_artifacts import load_prod_artifacts
from utils.logger import get_logger
from api.routes import router as prediction_router

LOG_DIR = Path("logs")
logger = get_logger(
    name="api",
    log_file=LOG_DIR / "api.log"
)

ARTIFACT_DIR = Path("artifacts/production")
ARTIFACTS = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading production artifacts")
    global ARTIFACTS
    ARTIFACTS = load_prod_artifacts(ARTIFACT_DIR)
    logger.info("Artifacts loaded successfully")
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