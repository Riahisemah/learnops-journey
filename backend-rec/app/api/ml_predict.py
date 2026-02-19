from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.schemas.ml import PredictionInput, PredictionOutput

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

@router.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """POST /api/ml/predict - Faire une prédiction avec le modèle ML"""
    
    try:
        # TODO: Charger et utiliser le vrai modèle ML
        # Pour l'instant, retourne une prédiction simulée
        
        # Exemple de logique simple
        prediction_value = 0.87
        
        return PredictionOutput(
            prediction=prediction_value,
            model_version="v1.0.0",
            confidence=0.95,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
