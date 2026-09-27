import time
import uuid
import json
import logging
import joblib
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from service.schemas import (
    PredictRequest,
    BatchPredictRequest,
    PredictResponse,
    BatchPredictResponse
)

logger = logging.getLogger("service_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)

MODEL_VERSION = "v1.0.0"
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup and cleanup on shutdown."""
    global model
    try:
        model = joblib.load("models/model_v1.pkl")
        logger.info(json.dumps({"event": "model_loaded", "version": MODEL_VERSION}))
    except Exception as e:
        logger.error(json.dumps({"event": "model_load_failed", "error": str(e)}))
        model = None
    yield

app = FastAPI(title="ITCS355 Lab 3 Model Service", lifespan=lifespan)

@app.middleware("http")
async def structured_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    log_entry = {
        "request_id": request_id,
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "latency_ms": latency_ms,
        "model_version": MODEL_VERSION
    }
    logger.info(json.dumps(log_entry))
    return response

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "alive"}

@app.get("/ready")
def readiness_check():
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not ready or failed to load"
        )
    return {"status": "ready", "model_version": MODEL_VERSION}

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not ready")
    
    prediction = model.predict([[payload.amount]])[0]
    return PredictResponse(
        is_fraud=bool(prediction),
        model_version=MODEL_VERSION
    )

@app.post("/predict/batch", response_model=BatchPredictResponse)
def predict_batch(payload: BatchPredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not ready")
    
    amounts = [[item.amount] for item in payload.items]
    predictions = model.predict(amounts)
    
    return BatchPredictResponse(
        predictions=[bool(p) for p in predictions],
        model_version=MODEL_VERSION
    )