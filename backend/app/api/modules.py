from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app.schemas.module import ModuleResponse, ModuleCreate, ModuleUpdate, LessonResponse
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.progression import LessonCompletion
from app.models.user import User
from app.api.deps import get_current_active_user, require_admin

router = APIRouter(prefix="/api/modules", tags=["Modules"])

def calculate_completion_rate(module: Module, user_id: str, db: Session) -> int:
    """Calculer le taux de complétion d'un module pour un utilisateur"""
    total_lessons = len(module.lessons)
    if total_lessons == 0:
        return 0
    
    completed_lessons = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == user_id,
        LessonCompletion.lesson_id.in_([lesson.id for lesson in module.lessons])
    ).count()
    
    return int((completed_lessons / total_lessons) * 100)

@router.get("", response_model=List[ModuleResponse])
async def get_modules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/modules - Liste tous les modules"""
    
    modules = db.query(Module).order_by(Module.week, Module.order).all()
    
    result = []
    for module in modules:
        # Enrichir les leçons avec le statut completed
        enriched_lessons = []
        for lesson in module.lessons:
            is_completed = db.query(LessonCompletion).filter(
                LessonCompletion.user_id == current_user.id,
                LessonCompletion.lesson_id == lesson.id
            ).first() is not None
            
            enriched_lessons.append(LessonResponse(
                id=lesson.id,
                title=lesson.title,
                type=lesson.type.value,
                duration=lesson.duration,
                completed=is_completed,
                url=lesson.url,
                content=lesson.content,
                description=lesson.content,
            ))

        completion_rate = calculate_completion_rate(module, current_user.id, db)
        
        result.append(ModuleResponse(
            id=module.id,
            title=module.title,
            description=module.description,
            week=module.week,
            order=module.order,
            lessons=enriched_lessons,
            completion_rate=completion_rate,
            total_duration=module.total_duration,
            icon=getattr(module, "icon", None),
        ))
    
    return result

@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(
    module_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/modules/{module_id} - Récupérer un module spécifique"""
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Enrichir les leçons
    enriched_lessons = []
    for lesson in module.lessons:
        is_completed = db.query(LessonCompletion).filter(
            LessonCompletion.user_id == current_user.id,
            LessonCompletion.lesson_id == lesson.id
        ).first() is not None
        
        enriched_lessons.append(LessonResponse(
            id=lesson.id,
            title=lesson.title,
            type=lesson.type.value,
            duration=lesson.duration,
            completed=is_completed,
            url=lesson.url,
            content=lesson.content,
            description=lesson.content,
        ))

    completion_rate = calculate_completion_rate(module, current_user.id, db)

    return ModuleResponse(
        id=module.id,
        title=module.title,
        description=module.description,
        week=module.week,
        order=module.order,
        lessons=enriched_lessons,
        completion_rate=completion_rate,
        total_duration=module.total_duration,
        icon=getattr(module, "icon", None),
    )


@router.post("", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
async def create_module(
    module_data: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """POST /api/modules - Créer un module (Admin uniquement)"""
    
    new_module = Module(
        id=f"module-{uuid.uuid4().hex[:8]}",
        title=module_data.title,
        description=module_data.description,
        week=module_data.week,
        order=module_data.order,
        total_duration=0
    )
    
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    
    return ModuleResponse(
        id=new_module.id,
        title=new_module.title,
        description=new_module.description,
        week=new_module.week,
        order=new_module.order,
        lessons=[],
        completion_rate=0,
        total_duration=0,
        icon=getattr(new_module, "icon", None),
    )

@router.put("/{module_id}", response_model=ModuleResponse)
async def update_module(
    module_id: str,
    module_data: ModuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """PUT /api/modules/{module_id} - Mettre à jour un module (Admin uniquement)"""
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    if module_data.title is not None:
        module.title = module_data.title
    if module_data.description is not None:
        module.description = module_data.description
    if module_data.week is not None:
        module.week = module_data.week
    if module_data.order is not None:
        module.order = module_data.order
    
    db.commit()
    db.refresh(module)
    
    return get_module(module_id, db, current_user)

@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(
    module_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """DELETE /api/modules/{module_id} - Supprimer un module (Admin uniquement)"""
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    db.delete(module)
    db.commit()
    return None

@router.get("/{module_id}/lessons", response_model=List[LessonResponse])
async def get_module_lessons(
    module_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/modules/{module_id}/lessons - Liste les leçons d'un module"""
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    enriched_lessons = []
    for lesson in module.lessons:
        is_completed = db.query(LessonCompletion).filter(
            LessonCompletion.user_id == current_user.id,
            LessonCompletion.lesson_id == lesson.id
        ).first() is not None
        
        enriched_lessons.append(LessonResponse(
            id=lesson.id,
            title=lesson.title,
            type=lesson.type.value,
            duration=lesson.duration,
            completed=is_completed,
            url=lesson.url,
            content=lesson.content,
            description=lesson.content,
        ))

    return enriched_lessons


@router.get("/{module_id}/lessons/{lesson_id}", response_model=LessonResponse)
async def get_module_lesson(
    module_id: str,
    lesson_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/modules/{module_id}/lessons/{lesson_id} - Get a single lesson by id"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.module_id == module_id
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    is_completed = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == current_user.id,
        LessonCompletion.lesson_id == lesson.id
    ).first() is not None
    return LessonResponse(
        id=lesson.id,
        title=lesson.title,
        type=lesson.type.value,
        duration=lesson.duration,
        completed=is_completed,
        url=lesson.url,
        content=lesson.content,
        description=lesson.content,
    )


@router.get("/{module_id}/lessons/{lesson_id}/content")
async def get_lesson_content(
    module_id: str,
    lesson_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/modules/{module_id}/lessons/{lesson_id}/content - Récupérer le contenu d'une leçon"""
    
    # Vérifier que le module existe
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Récupérer la leçon
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.module_id == module_id
    ).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Vérifier si la leçon est complétée
    is_completed = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == current_user.id,
        LessonCompletion.lesson_id == lesson.id
    ).first() is not None
    
    # Retourner le contenu selon le type
    return {
        "id": lesson.id,
        "title": lesson.title,
        "type": lesson.type.value,
        "duration": lesson.duration,
        "completed": is_completed,
        "url": lesson.url,
        "content": lesson.content,
        "moduleId": module_id,
        "lessonId": lesson_id,
        "theory": {
            "title": f"Théorie - {lesson.title}",
            "content": lesson.content or "Contenu théorique à venir...",
            "codeBlocks": [
                {
                    "language": "bash",
                    "code": "# Exemple de commande\n$ docker run hello-world"
                }
            ] if lesson.type.value == "practice" else []
        },
        "practice": {
            "title": f"Pratique - {lesson.title}",
            "content": lesson.content or "Exercices pratiques à venir...",
            "codeBlocks": [
                {
                    "language": "python",
                    "code": "# Exemple de code\ndef hello():\n    print('Hello, DevOps!')"
                }
            ] if lesson.type.value == "practice" else []
        }
    }