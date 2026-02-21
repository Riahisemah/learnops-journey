from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.schemas.admin import AdminStats, Analytics, RegistrationData, PopularModule, UserRoleCount, RecentActivity
from app.models.user import User
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.progression import UserProgression, LessonCompletion
from app.api.deps import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """GET /api/admin/stats - Statistiques du dashboard admin"""
    
    # Total users
    total_users = db.query(User).count()
    
    # Total modules
    total_modules = db.query(Module).count()
    
    # Total completions (leçons complétées)
    total_completions = db.query(LessonCompletion).count()
    
    # Average rating (simulé pour l'instant)
    average_rating = 4.8
    
    # Users growth (simulé - nouveaux users ce mois vs mois dernier)
    users_growth = 12
    
    # Completions rate
    total_lessons = sum([len(m.lessons) for m in db.query(Module).all()])
    if total_lessons > 0:
        completions_rate = (total_completions / (total_lessons * total_users)) * 100 if total_users > 0 else 0
    else:
        completions_rate = 0
    
    return AdminStats(
        total_users=total_users,
        total_modules=total_modules,
        total_completions=total_completions,
        average_rating=average_rating,
        users_growth=users_growth,
        completions_rate=round(completions_rate, 1)
    )

@router.get("/users")
async def get_admin_users(
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """GET /api/admin/users - Tableau utilisateurs avec filtres"""
    
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
    
    # Enrichir avec les progressions
    result = []
    for user in users:
        progression = db.query(UserProgression).filter(
            UserProgression.user_id == user.id
        ).first()
        
        result.append({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "progression": progression.progression if progression else 0
        })
    
    return result

@router.get("/analytics", response_model=Analytics)
async def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """GET /api/admin/analytics - Données analytiques détaillées"""
    
    # Registrations per day (last 7 days, portable date filter)
    registrations = []
    for i in range(7):
        day = (datetime.utcnow() - timedelta(days=i)).date()
        start = datetime.combine(day, datetime.min.time())
        end = start + timedelta(days=1)
        count = db.query(User).filter(
            User.created_at >= start,
            User.created_at < end,
        ).count()
        registrations.append(RegistrationData(
            date=day.strftime("%Y-%m-%d"),
            count=count,
        ))
    
    # Popular modules (simulé avec nombre de leçons complétées)
    popular_modules = []
    modules = db.query(Module).all()
    for module in modules:
        lesson_ids = [lesson.id for lesson in module.lessons]
        views = db.query(LessonCompletion).filter(
            LessonCompletion.lesson_id.in_(lesson_ids)
        ).count()
        
        popular_modules.append(PopularModule(
            module_id=module.id,
            title=module.title,
            views=views
        ))
    
    # Sort by views
    popular_modules.sort(key=lambda x: x.views, reverse=True)
    
    # User roles distribution
    user_roles = []
    for role in ["student", "instructor", "admin"]:
        count = db.query(User).filter(User.role == role).count()
        user_roles.append(UserRoleCount(role=role, count=count))
    
    # Recent activity: real data from lesson completions and new registrations
    recent_activity = []
    completions = (
        db.query(LessonCompletion, User, Lesson)
        .join(User, LessonCompletion.user_id == User.id)
        .join(Lesson, LessonCompletion.lesson_id == Lesson.id)
        .order_by(LessonCompletion.created_at.desc())
        .limit(8)
        .all()
    )
    for lc, u, lesson in completions:
        ts = getattr(lc, "created_at", None) or datetime.utcnow()
        recent_activity.append(
            RecentActivity(
                user=f"{u.first_name} {u.last_name}".strip() or u.email,
                action=f"completed {lesson.title}",
                timestamp=ts.isoformat() if hasattr(ts, "isoformat") else str(ts),
            )
        )
    new_users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )
    for u in new_users:
        recent_activity.append(
            RecentActivity(
                user=f"{u.first_name} {u.last_name}".strip() or u.email,
                action="registered",
                timestamp=u.created_at.isoformat() if u.created_at else datetime.utcnow().isoformat(),
            )
        )
    recent_activity.sort(key=lambda x: x.timestamp, reverse=True)
    recent_activity = recent_activity[:10]

    return Analytics(
        registrations_per_day=registrations,
        popular_modules=popular_modules[:5],  # Top 5
        user_roles=user_roles,
        recent_activity=recent_activity
    )
