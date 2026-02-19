from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import User
from app.models.progression import UserProgression
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """POST /api/auth/register - Inscription d'un nouvel utilisateur"""
    
    # Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Créer l'utilisateur
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Créer la progression initiale
    progression = UserProgression(
        id=str(uuid.uuid4()),
        user_id=new_user.id,
        progression=0,
        modules_completed=[],
        time_spent=0
    )
    db.add(progression)
    db.commit()
    
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """POST /api/auth/login - Connexion utilisateur"""
    
    # Trouver l'utilisateur
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Vérifier les credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Vérifier si actif
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Mettre à jour last_login
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    # Créer le token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """GET /api/auth/me - Récupérer le profil utilisateur connecté"""
    return current_user

@router.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    """POST /api/auth/forgot-password - Demander une réinitialisation"""
    # Toujours retourner succès pour la sécurité
    return {"message": "Password reset email sent"}
