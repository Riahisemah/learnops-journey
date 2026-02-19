from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/api/bookmarks", tags=["Bookmarks"])

# Stockage temporaire des favoris
bookmarks_store = []

class Bookmark:
    def __init__(self, id: str, user_id: str, resource_type: str, resource_id: str, title: str):
        self.id = id
        self.user_id = user_id
        self.resource_type = resource_type  # "module", "lesson", "quiz"
        self.resource_id = resource_id
        self.title = title
        self.created_at = datetime.utcnow().isoformat()

@router.post("")
async def add_bookmark(
    resource_type: str,
    resource_id: str,
    title: str,
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/bookmarks - Ajouter un favori"""
    
    # Vérifier si déjà en favoris
    existing = any(
        b.user_id == current_user.id and 
        b.resource_type == resource_type and 
        b.resource_id == resource_id
        for b in bookmarks_store
    )
    
    if existing:
        raise HTTPException(status_code=400, detail="Déjà dans les favoris")
    
    bookmark = Bookmark(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        resource_type=resource_type,
        resource_id=resource_id,
        title=title
    )
    
    bookmarks_store.append(bookmark)
    
    return {
        "id": bookmark.id,
        "resource_type": bookmark.resource_type,
        "resource_id": bookmark.resource_id,
        "title": bookmark.title,
        "created_at": bookmark.created_at
    }

@router.get("/me")
async def get_my_bookmarks(
    current_user: User = Depends(get_current_active_user),
    resource_type: str = None
):
    """GET /api/bookmarks/me - Mes favoris (avec filtre optionnel par type)"""
    
    user_bookmarks = [
        {
            "id": b.id,
            "resource_type": b.resource_type,
            "resource_id": b.resource_id,
            "title": b.title,
            "created_at": b.created_at
        }
        for b in bookmarks_store
        if b.user_id == current_user.id and (
            resource_type is None or b.resource_type == resource_type
        )
    ]
    
    # Trier par date (plus récent en premier)
    user_bookmarks.sort(key=lambda x: x["created_at"], reverse=True)
    
    return user_bookmarks

@router.delete("/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """DELETE /api/bookmarks/{id} - Retirer des favoris"""
    
    for i, bookmark in enumerate(bookmarks_store):
        if bookmark.id == bookmark_id and bookmark.user_id == current_user.id:
            bookmarks_store.pop(i)
            return {"message": "Favori supprimé"}
    
    raise HTTPException(status_code=404, detail="Favori introuvable")

@router.get("/check")
async def check_bookmark(
    resource_type: str,
    resource_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/bookmarks/check - Vérifier si une ressource est en favoris"""
    
    is_bookmarked = any(
        b.user_id == current_user.id and 
        b.resource_type == resource_type and 
        b.resource_id == resource_id
        for b in bookmarks_store
    )
    
    return {"is_bookmarked": is_bookmarked}
