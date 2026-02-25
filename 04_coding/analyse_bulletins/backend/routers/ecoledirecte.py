from __future__ import annotations
"""
Routes de synchronisation avec EcoleDirecte.
Le token ED est recréé à chaque appel (credentials stockés chiffrés).
"""
import uuid
from typing import List, Tuple
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from routers.auth import get_current_teacher
from services.ecoledirecte_client import EcoleDirecteClient, EcoleDirecteError
from services.crypto import decrypt

router = APIRouter(prefix="/api/ecoledirecte", tags=["ecoledirecte"])


def _login_ed(teacher: models.Teacher) -> Tuple[EcoleDirecteClient, str, list]:
    """Décrypte les credentials, re-authentifie et retourne (client, token, classes)."""
    password = decrypt(teacher.encrypted_password)
    client = EcoleDirecteClient()
    try:
        ed_info = client.login(teacher.ecoledirecte_login, password)
        return client, ed_info["token"], ed_info.get("classes", [])
    except EcoleDirecteError as e:
        client.close()
        raise HTTPException(status_code=502, detail=f"EcoleDirecte : {e}")


def _get_ed_client_and_token(teacher: models.Teacher) -> Tuple[EcoleDirecteClient, str]:
    """Décrypte les credentials et re-authentifie auprès d'EcoleDirecte."""
    client, token, _ = _login_ed(teacher)
    return client, token


@router.post("/sync-classes", response_model=List[schemas.ClasseOut])
def sync_classes(
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """
    Récupère les classes depuis EcoleDirecte (via la réponse de login) et les synchronise en base.
    """
    client, _, ed_classes = _login_ed(teacher)
    client.close()

    if not ed_classes:
        raise HTTPException(status_code=502, detail="Aucune classe trouvée dans la réponse EcoleDirecte")

    synced = []
    for ec in ed_classes:
        classe = (
            db.query(models.Classe)
            .filter(
                models.Classe.teacher_id == teacher.id,
                models.Classe.ecoledirecte_id == ec["id"],
            )
            .first()
        )
        if not classe:
            classe = models.Classe(
                id=str(uuid.uuid4()),
                teacher_id=teacher.id,
                ecoledirecte_id=ec["id"],
            )
            db.add(classe)
        classe.name = ec["name"]
        classe.annee_scolaire = ec["annee_scolaire"]
        db.commit()
        db.refresh(classe)
        synced.append(classe)

    return synced


@router.get("/classes", response_model=List[schemas.ClasseOut])
def list_classes(
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """Retourne les classes déjà synchronisées en base."""
    return (
        db.query(models.Classe)
        .filter(models.Classe.teacher_id == teacher.id)
        .all()
    )


@router.post("/classes/{classe_id}/sync-students", response_model=List[schemas.StudentOut])
def sync_students(
    classe_id: str,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """
    Récupère les élèves d'une classe depuis EcoleDirecte et les synchronise en base.
    """
    classe = db.query(models.Classe).filter(
        models.Classe.id == classe_id,
        models.Classe.teacher_id == teacher.id,
    ).first()
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    client, token = _get_ed_client_and_token(teacher)
    try:
        ed_students = client.get_students(token, classe.ecoledirecte_id)
    except EcoleDirecteError as e:
        raise HTTPException(status_code=502, detail=str(e))
    finally:
        client.close()

    synced = []
    for es in ed_students:
        student = (
            db.query(models.Student)
            .filter(
                models.Student.classe_id == classe_id,
                models.Student.ecoledirecte_id == str(es["id"]),
            )
            .first()
        )
        if not student:
            student = models.Student(
                id=str(uuid.uuid4()),
                classe_id=classe_id,
                ecoledirecte_id=str(es["id"]),
            )
            db.add(student)
        student.first_name = es["first_name"]
        student.last_name = es["last_name"]
        db.commit()
        db.refresh(student)
        synced.append(student)

    return synced


@router.get("/classes/{classe_id}/students", response_model=List[schemas.StudentOut])
def list_students(
    classe_id: str,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """Retourne les élèves déjà synchronisés en base pour une classe."""
    classe = db.query(models.Classe).filter(
        models.Classe.id == classe_id,
        models.Classe.teacher_id == teacher.id,
    ).first()
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    return db.query(models.Student).filter(models.Student.classe_id == classe_id).all()
