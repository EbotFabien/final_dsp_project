from pydantic import BaseModel
from typing import List, Dict, Any

class PredictionRequest(BaseModel):
    features: List[Dict[str, float]]

class PredictionResponse(BaseModel):
    predictions: List[float]

class PastPredictionResponse(BaseModel):
    id: int
    input_features: Dict[str, Any]
    prediction: float
    model_name: str
    created_at: str
