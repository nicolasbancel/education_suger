from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from services.crypto import encrypt, decrypt
from services.ecoledirecte_client import EcoleDirecteClient, EcoleDirecteError

router = APIRouter(prefix="/api/auth", tags=["auth"])


async def get_current_teacher(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
) -> models.Teacher:
    token = authorization.replace("Bearer ", "")
    teacher = (
        db.query(models.Teacher)
        .filter(models.Teacher.session_token == token)
        .first()
    )
    if not teacher:
        raise HTTPException(status_code=401, detail="Session invalide ou expirée")
    return teacher


@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Authentifie le professeur : vérifie ses credentials EcoleDirecte,
    les stocke chiffrés, et retourne un session_token.
    """
    # Vérification des credentials EcoleDirecte
    client = EcoleDirecteClient()
    try:
        ed_info = client.login(request.ecoledirecte_login, request.ecoledirecte_password)
    except EcoleDirecteError as e:
        raise HTTPException(status_code=401, detail=f"Échec connexion EcoleDirecte : {e}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"EcoleDirecte inaccessible : {e}")
    finally:
        client.close()

    # Upsert teacher
    teacher = (
        db.query(models.Teacher)
        .filter(models.Teacher.ecoledirecte_login == request.ecoledirecte_login)
        .first()
    )
    if not teacher:
        teacher = models.Teacher(id=str(uuid.uuid4()))
        db.add(teacher)

    teacher.ecoledirecte_login = request.ecoledirecte_login
    teacher.encrypted_password = encrypt(request.ecoledirecte_password)
    teacher.ed_account_id = ed_info["account_id"]
    teacher.session_token = str(uuid.uuid4())
    db.commit()
    db.refresh(teacher)

    return schemas.LoginResponse(
        session_token=teacher.session_token,
        teacher_id=teacher.id,
    )


@router.get("/me")
def me(teacher: models.Teacher = Depends(get_current_teacher)):
    return {
        "teacher_id": teacher.id,
        "login": teacher.ecoledirecte_login,
        "ed_account_id": teacher.ed_account_id,
    }
