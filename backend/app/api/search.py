from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.quiz import Quiz

router = APIRouter(prefix="/api/search", tags=["Search"])

@router.get("")
async def global_search(
    q: str = Query(..., min_length=2, description="Terme de recherche"),
    db: Session = Depends(get_db),
    limit: int = 20
):
    """GET /api/search?q=docker - Recherche globale dans modules, leçons et quiz"""
    
    if not q or len(q.strip()) < 2:
        return {
            "query": q,
            "results": {
                "modules": [],
                "lessons": [],
                "quizzes": []
            }
        }
    
    search_term = f"%{q.lower()}%"
    
    # Rechercher dans les modules
    modules = db.query(Module).filter(
        (Module.title.ilike(search_term)) |
        (Module.description.ilike(search_term))
    ).limit(limit).all()
    
    # Rechercher dans les leçons
    lessons = db.query(Lesson).filter(
        (Lesson.title.ilike(search_term)) |
        (Lesson.content.ilike(search_term))
    ).limit(limit).all()
    
    # Rechercher dans les quiz
    quizzes = db.query(Quiz).filter(
        Quiz.title.ilike(search_term)
    ).limit(limit).all()
    
    return {
        "query": q,
        "total": len(modules) + len(lessons) + len(quizzes),
        "results": {
            "modules": [
                {
                    "id": m.id,
                    "title": m.title,
                    "description": m.description,
                    "week": m.week,
                    "type": "module"
                }
                for m in modules
            ],
            "lessons": [
                {
                    "id": l.id,
                    "title": l.title,
                    "type": l.type,
                    "module_id": l.module_id,
                    "duration": l.duration,
                    "result_type": "lesson"
                }
                for l in lessons
            ],
            "quizzes": [
                {
                    "id": q.id,
                    "title": q.title,
                    "module_id": q.module_id,
                    "type": "quiz"
                }
                for q in quizzes
            ]
        }
    }
