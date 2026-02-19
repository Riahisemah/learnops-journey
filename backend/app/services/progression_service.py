"""
Service de gestion de la progression utilisateur
"""
from sqlalchemy.orm import Session
from app.models.progression import UserProgression, UserBadge, LessonCompletion
from app.models.module import Module
from app.models.lesson import Lesson
import uuid


def calculate_user_progression(db: Session, user_id: str) -> dict:
    """Calcule la progression globale d'un utilisateur"""
    
    # Récupérer la progression
    progression = db.query(UserProgression).filter(
        UserProgression.user_id == user_id
    ).first()
    
    if not progression:
        # Créer si n'existe pas
        progression = UserProgression(
            id=str(uuid.uuid4()),
            user_id=user_id,
            progression=0,
            modules_completed=[],
            time_spent=0
        )
        db.add(progression)
        db.commit()
        db.refresh(progression)
    
    # Compter les leçons complétées
    completed_lessons = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == user_id,
        LessonCompletion.completed == 1
    ).count()
    
    # Compter le total de leçons
    total_lessons = db.query(Lesson).count()
    
    # Calculer le pourcentage
    if total_lessons > 0:
        progression_percentage = int((completed_lessons / total_lessons) * 100)
    else:
        progression_percentage = 0
    
    # Mettre à jour
    progression.progression = progression_percentage
    db.commit()
    
    # Récupérer les badges
    badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()
    badge_names = [badge.badge_name for badge in badges]
    
    return {
        "user_id": user_id,
        "progression": progression_percentage,
        "modules_completed": progression.modules_completed or [],
        "badges": badge_names,
        "time_spent": progression.time_spent,
        "lessons_completed": completed_lessons,
        "total_lessons": total_lessons
    }


def award_badge(db: Session, user_id: str, badge_name: str) -> bool:
    """Attribuer un badge à un utilisateur"""
    
    # Vérifier si le badge existe déjà
    existing = db.query(UserBadge).filter(
        UserBadge.user_id == user_id,
        UserBadge.badge_name == badge_name
    ).first()
    
    if existing:
        return False
    
    # Créer le badge
    badge = UserBadge(
        id=str(uuid.uuid4()),
        user_id=user_id,
        badge_name=badge_name
    )
    db.add(badge)
    db.commit()
    
    return True


def check_and_award_badges(db: Session, user_id: str):
    """Vérifier et attribuer automatiquement les badges"""
    
    progression = calculate_user_progression(db, user_id)
    
    # Badge première leçon
    if progression["lessons_completed"] >= 1:
        award_badge(db, user_id, "first-lesson")
    
    # Badge 5 leçons
    if progression["lessons_completed"] >= 5:
        award_badge(db, user_id, "5-lessons")
    
    # Badge 10 leçons
    if progression["lessons_completed"] >= 10:
        award_badge(db, user_id, "10-lessons")
    
    # Badge module complet
    if progression["progression"] >= 25:
        award_badge(db, user_id, "module-complete")
    
    # Badge 50% progression
    if progression["progression"] >= 50:
        award_badge(db, user_id, "half-way")
    
    # Badge 100% progression
    if progression["progression"] >= 100:
        award_badge(db, user_id, "completion-master")
