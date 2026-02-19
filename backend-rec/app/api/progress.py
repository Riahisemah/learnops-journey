from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.progression import UserProgressionResponse, ProgressUpdate
from app.models.progression import UserProgression, UserBadge
from app.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/api/progress", tags=["Progress"])

@router.get("/me", response_model=UserProgressionResponse)
async def get_my_progression(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/progress/me - Récupérer la progression de l'utilisateur connecté"""
    
    progression = db.query(UserProgression).filter(
        UserProgression.user_id == current_user.id
    ).first()
    
    if not progression:
        raise HTTPException(status_code=404, detail="Progression not found")
    
    # Récupérer les badges
    badges = db.query(UserBadge).filter(UserBadge.user_id == current_user.id).all()
    badge_names = [badge.badge_name for badge in badges]
    
    return UserProgressionResponse(
        user_id=current_user.id,
        progression=progression.progression,
        modules_completed=progression.modules_completed or [],
        badges=badge_names,
        time_spent=progression.time_spent
    )

@router.post("/update")
async def update_progression(
    progress_data: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/progress/update - Mettre à jour la progression"""
    
    progression = db.query(UserProgression).filter(
        UserProgression.user_id == current_user.id
    ).first()
    
    if not progression:
        raise HTTPException(status_code=404, detail="Progression not found")
    
    progression.progression = progress_data.progression
    progression.modules_completed = progress_data.modules_completed
    progression.time_spent = progress_data.time_spent
    
    db.commit()
    
    return {"message": "Progression updated successfully"}
