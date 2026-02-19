from pydantic import BaseModel
from typing import Dict, Union

class PredictionInput(BaseModel):
    features: Dict[str, Union[int, float, str]]

class PredictionOutput(BaseModel):
    prediction: Union[int, float, str]
    model_version: str
    confidence: float
    timestamp: str
