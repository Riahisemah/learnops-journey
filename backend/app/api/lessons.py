from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.lesson import Lesson
from app.models.progression import LessonCompletion
from app.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/api/lessons", tags=["Lessons"])

@router.post("/{lesson_id}/complete", status_code=status.HTTP_200_OK)
async def complete_lesson(
    lesson_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/lessons/{lesson_id}/complete - Marquer une leçon comme complétée"""
    
    # Vérifier que la leçon existe
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Vérifier si déjà complétée
    existing_completion = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == current_user.id,
        LessonCompletion.lesson_id == lesson_id
    ).first()
    
    if existing_completion:
        return {"message": "Lesson already completed"}
    
    # Créer la completion
    completion = LessonCompletion(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        lesson_id=lesson_id,
        completed=1
    )
    
    db.add(completion)
    db.commit()
    
    return {"message": "Lesson marked as complete"}
