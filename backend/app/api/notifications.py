from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])

# Temporairement, stockage en mémoire (à remplacer par DB)
notifications_store = []

class Notification:
    def __init__(self, id: str, user_id: str, title: str, message: str, type: str = "info"):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = type
        self.read = False
        self.created_at = datetime.utcnow().isoformat()

@router.post("")
async def create_notification(
    title: str,
    message: str,
    user_id: Optional[str] = None,
    type: str = "info",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/notifications - Créer une notification"""
    
    # Si user_id n'est pas spécifié, notifier l'utilisateur courant
    target_user_id = user_id or current_user.id
    
    notification = Notification(
        id=str(uuid.uuid4()),
        user_id=target_user_id,
        title=title,
        message=message,
        type=type
    )
    
    notifications_store.append(notification)
    
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "title": notification.title,
        "message": notification.message,
        "type": notification.type,
        "read": notification.read,
        "created_at": notification.created_at
    }

@router.get("/me")
async def get_my_notifications(
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/notifications/me - Récupérer mes notifications"""
    
    user_notifications = [
        {
            "id": notif.id,
            "title": notif.title,
            "message": notif.message,
            "type": notif.type,
            "read": notif.read,
            "created_at": notif.created_at
        }
        for notif in notifications_store
        if notif.user_id == current_user.id
    ]
    
    # Trier par date (plus récent en premier)
    user_notifications.sort(key=lambda x: x["created_at"], reverse=True)
    
    return user_notifications

@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """PUT /api/notifications/{id}/read - Marquer comme lue"""
    
    for notif in notifications_store:
        if notif.id == notification_id and notif.user_id == current_user.id:
            notif.read = True
            return {"message": "Notification marked as read"}
    
    raise HTTPException(status_code=404, detail="Notification not found")

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """DELETE /api/notifications/{id} - Supprimer une notification"""
    
    for i, notif in enumerate(notifications_store):
        if notif.id == notification_id and notif.user_id == current_user.id:
            notifications_store.pop(i)
            return {"message": "Notification deleted"}
    
    raise HTTPException(status_code=404, detail="Notification not found")

@router.get("/unread/count")
async def get_unread_count(
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/notifications/unread/count - Compter les notifications non lues"""
    
    count = sum(
        1 for notif in notifications_store
        if notif.user_id == current_user.id and not notif.read
    )
    
    return {"count": count}
