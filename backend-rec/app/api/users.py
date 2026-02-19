from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.progression import UserProgressionResponse
from app.models.user import User, UserRole
from app.models.progression import UserProgression, UserBadge
from app.api.deps import get_current_active_user, require_admin

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
async def get_users(
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """GET /api/users - Liste tous les utilisateurs (Admin uniquement)"""
    
    query = db.query(User)
    
    # Filtres
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (User.first_name.ilike(search_pattern)) |
            (User.last_name.ilike(search_pattern)) |
            (User.email.ilike(search_pattern))
        )
    
    users = query.all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/users/{user_id} - Récupérer un utilisateur spécifique"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """PUT /api/users/{user_id} - Mettre à jour un utilisateur"""
    
    # Vérifier que l'utilisateur modifie son propre profil ou est admin
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Mettre à jour les champs
    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.avatar is not None:
        user.avatar = user_data.avatar
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """DELETE /api/users/{user_id} - Supprimer un utilisateur (Admin uniquement)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None

@router.get("/{user_id}/progression", response_model=UserProgressionResponse)
async def get_user_progression(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/users/{user_id}/progression - Récupérer la progression"""
    
    progression = db.query(UserProgression).filter(
        UserProgression.user_id == user_id
    ).first()
    
    if not progression:
        raise HTTPException(status_code=404, detail="Progression not found")
    
    # Récupérer les badges
    badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()
    badge_names = [badge.badge_name for badge in badges]
    
    return {
        "user_id": user_id,
        "progression": progression.progression,
        "modules_completed": progression.modules_completed or [],
        "badges": badge_names,
        "time_spent": progression.time_spent
    }
