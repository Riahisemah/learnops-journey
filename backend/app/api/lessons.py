from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.lesson import Lesson, LessonType
from app.models.module import Module
from app.models.quiz import Quiz
from app.models.progression import LessonCompletion
from app.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter(tags=["Lessons"])

# ─── /api/lessons/{lesson_id}/complete ────────────────────────────────────────

@router.post("/api/lessons/{lesson_id}/complete", status_code=status.HTTP_200_OK)
async def complete_lesson(
    lesson_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/lessons/{lesson_id}/complete - Marquer une leçon comme complétée"""

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    existing = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == current_user.id,
        LessonCompletion.lesson_id == lesson_id
    ).first()

    if existing:
        return {"message": "Lesson already completed"}

    completion = LessonCompletion(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        lesson_id=lesson_id,
        completed=1
    )

    db.add(completion)
    db.commit()

    return {"message": "Lesson marked as complete"}


# ─── /api/modules/{module_id}/lessons/{lesson_id}/content ─────────────────────
# This is the route the frontend calls — was missing entirely.

@router.get("/api/modules/{module_id}/lessons/{lesson_id}/content")
async def get_lesson_content(
    module_id: str,
    lesson_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    GET /api/modules/{module_id}/lessons/{lesson_id}/content
    Returns full lesson content including theory, practice, video data, and quiz questions.
    """

    # Verify module exists
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Verify lesson exists and belongs to module
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.module_id == module_id
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Check if lesson is already completed by this user
    completion = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == current_user.id,
        LessonCompletion.lesson_id == lesson_id
    ).first()

    # Base response — always included
    response = {
        "id": lesson.id,
        "module_id": lesson.module_id,
        "title": lesson.title,
        "type": lesson.type.value,
        "duration": lesson.duration,
        "order": lesson.order,
        "is_completed": bool(completion),
        "content": None,
        "video": None,
        "quiz": None,
    }

    # ── TEXT / PRACTICE lessons → return the content field ────────────────────
    if lesson.type in (LessonType.TEXT, LessonType.PRACTICE):
        response["content"] = {
            "theory": {
                "title": lesson.title,
                "body": lesson.content or "",
            },
            "practice": None,   # practice instructions are embedded in content
        }

    # ── VIDEO lessons → return embed URL + chapters ───────────────────────────
    elif lesson.type == LessonType.VIDEO:
        VIDEO_CHAPTERS = {
            "cicd-github-actions": [
                {"time": 0,   "title": "Introduction"},
                {"time": 60,  "title": "Créer un workflow"},
                {"time": 180, "title": "Jobs et steps"},
                {"time": 300, "title": "Variables et secrets"},
                {"time": 420, "title": "Déploiement automatique"},
            ],
            "dvc-versioning": [
                {"time": 0,   "title": "Pourquoi versionner les données ?"},
                {"time": 90,  "title": "Installation de DVC"},
                {"time": 200, "title": "dvc init & dvc add"},
                {"time": 350, "title": "Remote storage"},
                {"time": 480, "title": "Pipelines DVC"},
            ],
            "fastapi-ml": [
                {"time": 0,   "title": "Introduction à FastAPI"},
                {"time": 75,  "title": "Premier endpoint"},
                {"time": 180, "title": "Schémas Pydantic"},
                {"time": 300, "title": "Charger un modèle ML"},
                {"time": 420, "title": "Endpoint de prédiction"},
            ],
            "cloud-deployment": [
                {"time": 0,   "title": "Aperçu des options cloud"},
                {"time": 120, "title": "AWS Deployment"},
                {"time": 280, "title": "Google Cloud Run"},
                {"time": 400, "title": "Azure Container Instances"},
                {"time": 520, "title": "Comparaison et choix"},
            ],
        }

        response["video"] = {
            "embed_url": lesson.url,
            "chapters": VIDEO_CHAPTERS.get(lesson.id, []),
        }

    # ── QUIZ lessons → return quiz questions (without correct answers) ─────────
    elif lesson.type == LessonType.QUIZ:
        quiz = db.query(Quiz).filter(Quiz.module_id == module_id).order_by(Quiz.id).first()

        if quiz:
            # Strip correct_answers so the frontend can't cheat
            safe_questions = []
            for q in (quiz.questions or []):
                safe_questions.append({
                    "id": q["id"],
                    "question": q["question"],
                    "type": q["type"],
                    "options": q["options"],
                    # correct_answers intentionally omitted
                    "explanation": q.get("explanation", ""),
                })

            response["quiz"] = {
                "quiz_id": quiz.id,
                "title": quiz.title,
                "passing_score": quiz.passing_score,
                "time_limit": quiz.time_limit,
                "questions": safe_questions,
            }

    return response


# ─── /api/modules/{module_id}/lessons  (list all lessons in a module) ─────────

@router.get("/api/modules/{module_id}/lessons")
async def get_module_lessons(
    module_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    GET /api/modules/{module_id}/lessons
    Returns all lessons for a module, with completion status for the current user.
    """

    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    lessons = db.query(Lesson).filter(
        Lesson.module_id == module_id
    ).order_by(Lesson.order).all()

    # Get all completions for this user in one query
    lesson_ids = [l.id for l in lessons]
    completions = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == current_user.id,
        LessonCompletion.lesson_id.in_(lesson_ids)
    ).all()
    completed_ids = {c.lesson_id for c in completions}

    return [
        {
            "id": lesson.id,
            "module_id": lesson.module_id,
            "title": lesson.title,
            "type": lesson.type.value,
            "duration": lesson.duration,
            "order": lesson.order,
            "is_completed": lesson.id in completed_ids,
            "url": lesson.url,
        }
        for lesson in lessons
    ]