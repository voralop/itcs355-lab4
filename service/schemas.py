from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be greater than 0")

class BatchPredictRequest(BaseModel):
    items: List[PredictRequest] = Field(..., max_length=100, description="Max 100 transactions allowed per batch")

class PredictResponse(BaseModel):
    is_fraud: bool
    model_version: str

class BatchPredictResponse(BaseModel):
    predictions: List[bool]
    model_version: str