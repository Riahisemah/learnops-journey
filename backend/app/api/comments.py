from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.database import get_db
from app.models.user import User, UserRole
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/api/lessons", tags=["Lesson Comments"])

# Stockage temporaire des commentaires (à remplacer par DB)
comments_store = []

class Comment:
    def __init__(self, id: str, lesson_id: str, user_id: str, user_name: str, content: str):
        self.id = id
        self.lesson_id = lesson_id
        self.user_id = user_id
        self.user_name = user_name
        self.content = content
        self.created_at = datetime.utcnow().isoformat()

@router.post("/{lesson_id}/comments")
async def add_comment(
    lesson_id: str,
    content: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/lessons/{id}/comments - Ajouter un commentaire"""
    
    if not content or len(content.strip()) == 0:
        raise HTTPException(status_code=400, detail="Le commentaire ne peut pas être vide")
    
    comment = Comment(
        id=str(uuid.uuid4()),
        lesson_id=lesson_id,
        user_id=current_user.id,
        user_name=f"{current_user.first_name} {current_user.last_name}",
        content=content.strip()
    )
    
    comments_store.append(comment)
    
    return {
        "id": comment.id,
        "lesson_id": comment.lesson_id,
        "user_id": comment.user_id,
        "user_name": comment.user_name,
        "content": comment.content,
        "created_at": comment.created_at
    }

@router.get("/{lesson_id}/comments")
async def get_comments(
    lesson_id: str,
    skip: int = 0,
    limit: int = 50
):
    """GET /api/lessons/{id}/comments - Lister les commentaires d'une leçon"""
    
    lesson_comments = [
        {
            "id": comment.id,
            "lesson_id": comment.lesson_id,
            "user_id": comment.user_id,
            "user_name": comment.user_name,
            "content": comment.content,
            "created_at": comment.created_at
        }
        for comment in comments_store
        if comment.lesson_id == lesson_id
    ]
    
    # Trier par date (plus récent en premier)
    lesson_comments.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Pagination
    return {
        "total": len(lesson_comments),
        "comments": lesson_comments[skip:skip + limit]
    }

@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """DELETE /api/comments/{id} - Supprimer un commentaire (auteur ou admin)"""
    
    for i, comment in enumerate(comments_store):
        if comment.id == comment_id:
            # Vérifier que l'utilisateur est l'auteur ou admin
            if comment.user_id != current_user.id and current_user.role != UserRole.ADMIN:
                raise HTTPException(status_code=403, detail="Non autorisé")
            
            comments_store.pop(i)
            return {"message": "Commentaire supprimé"}
    
    raise HTTPException(status_code=404, detail="Commentaire introuvable")
