from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime
from io import BytesIO
import uuid

from app.database import get_db
from app.models.user import User
from app.models.progression import UserProgression
from app.api.deps import get_current_active_user
from app.services.progression_service import calculate_user_progression

router = APIRouter(prefix="/api/certificates", tags=["Certificates"])

# Stockage temporaire des certificats
certificates_store = {}

@router.post("/generate")
async def generate_certificate(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/certificates/generate - Générer un certificat si progression = 100%"""
    
    # Calculer la progression
    progression_data = calculate_user_progression(db, current_user.id)
    
    if progression_data["progression"] < 100:
        raise HTTPException(
            status_code=400,
            detail=f"Progression insuffisante. Vous êtes à {progression_data['progression']}%"
        )
    
    # Générer un certificat
    certificate_id = str(uuid.uuid4())
    certificate_data = {
        "id": certificate_id,
        "user_id": current_user.id,
        "user_name": f"{current_user.first_name} {current_user.last_name}",
        "generated_at": datetime.utcnow().isoformat(),
        "modules_completed": progression_data["modules_completed"],
        "badges": progression_data["badges"]
    }
    
    certificates_store[certificate_id] = certificate_data
    
    return {
        "certificate_id": certificate_id,
        "message": "Certificat généré avec succès",
        "download_url": f"/api/certificates/{certificate_id}"
    }

@router.get("/me")
async def get_my_certificates(
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/certificates/me - Lister mes certificats"""
    
    user_certificates = [
        cert for cert in certificates_store.values()
        if cert["user_id"] == current_user.id
    ]
    
    return user_certificates

@router.get("/{certificate_id}")
async def download_certificate(
    certificate_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/certificates/{id} - Télécharger le certificat (format JSON pour l'instant)"""
    
    certificate = certificates_store.get(certificate_id)
    
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificat introuvable")
    
    if certificate["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Pour l'instant, retourner JSON
    # TODO: Générer un vrai PDF avec ReportLab
    return certificate

@router.delete("/{certificate_id}")
async def delete_certificate(
    certificate_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """DELETE /api/certificates/{id} - Supprimer un certificat"""
    
    certificate = certificates_store.get(certificate_id)
    
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificat introuvable")
    
    if certificate["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    del certificates_store[certificate_id]
    
    return {"message": "Certificat supprimé"}
