from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.progression import UserProgressionResponse, ProgressUpdate
from app.models.progression import UserProgression, UserBadge
from app.models.user import User
from app.api.deps import get_current_active_user
from app.services.progression_service import (
    calculate_user_progression,
    check_and_award_badges
)

router = APIRouter(prefix="/api/progress", tags=["Progress"])

@router.get("/me")
async def get_my_progression(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/progress/me - Récupérer la progression de l'utilisateur connecté avec calcul automatique"""
    
    # Calculer la progression en temps réel
    progression_data = calculate_user_progression(db, current_user.id)
    
    # Vérifier et attribuer les badges automatiquement
    check_and_award_badges(db, current_user.id)
    
    # Re-calculer pour inclure les nouveaux badges
    progression_data = calculate_user_progression(db, current_user.id)
    
    return progression_data

@router.post("/update")
async def update_progression(
    progress_data: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/progress/update - Mettre à jour la progression manuellement"""
    
    progression = db.query(UserProgression).filter(
        UserProgression.user_id == current_user.id
    ).first()
    
    if not progression:
        raise HTTPException(status_code=404, detail="Progression not found")
    
    # Mettre à jour les champs
    if progress_data.progression is not None:
        progression.progression = progress_data.progression
    if progress_data.modules_completed is not None:
        progression.modules_completed = progress_data.modules_completed
    if progress_data.time_spent is not None:
        progression.time_spent = progress_data.time_spent
    
    db.commit()
    
    # Vérifier les badges après mise à jour
    check_and_award_badges(db, current_user.id)
    
    # Retourner la progression mise à jour
    progression_data = calculate_user_progression(db, current_user.id)
    return progression_data
