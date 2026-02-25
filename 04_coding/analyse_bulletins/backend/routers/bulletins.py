from __future__ import annotations
"""
Routes pour la récupération des données de bulletins via l'API EcoleDirecte.
Les données (notes, appréciations, vie scolaire) sont récupérées directement
en JSON — plus de téléchargement PDF ni d'extraction LLM factuelle.
La tâche tourne en background avec suivi de progression.
"""
import uuid
import time
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from routers.auth import get_current_teacher
from services.ecoledirecte_client import EcoleDirecteClient, EcoleDirecteError
from services.crypto import decrypt

router = APIRouter(prefix="/api/bulletins", tags=["bulletins"])

# Suivi des jobs en mémoire (suffisant pour MVP local mono-utilisateur)
_jobs: Dict[str, schemas.JobStatus] = {}

# Mapping période EcoleDirecte → numéro de trimestre
_PERIODE_MAP = {"A001": 1, "A002": 2, "A003": 3}


def _fetch_bulletins_job(
    job_id: str,
    ed_login: str,
    encrypted_password: bytes,
    classe_id: str,
    trimestre: int,
    students: List[models.Student],
    annee_scolaire: str,
    db_url: str,
):
    """Tâche de fond : récupère les notes/appréciations via notes.awp + viescolaire.awp."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    LocalSession = sessionmaker(bind=engine)
    db = LocalSession()

    job = _jobs[job_id]
    job.total = len(students)

    password = decrypt(encrypted_password)
    client = EcoleDirecteClient()
    periode_id = f"A00{trimestre}"

    try:
        ed_info = client.login(ed_login, password)
        token = ed_info["token"]
    except Exception as e:
        job.status = "error"
        job.errors.append(f"Login EcoleDirecte échoué : {e}")
        client.close()
        db.close()
        return

    for student in students:
        try:
            eleve_id = int(student.ecoledirecte_id)

            # Récupération notes + appréciations
            notes_data = client.get_student_notes(token, eleve_id, annee_scolaire)
            periodes = notes_data.get("periodes", [])
            periode = next((p for p in periodes if p.get("idPeriode") == periode_id), None)

            if not periode:
                job.errors.append(
                    f"{student.last_name} {student.first_name} : période {periode_id} introuvable"
                )
                job.progress += 1
                continue

            em = periode.get("ensembleMatieres", {})

            # Récupération vie scolaire (absences/retards)
            vs_data = client.get_student_vie_scolaire(token, eleve_id)
            absences_total = _count_absences(vs_data, periode_id)
            retards_total = _count_retards(vs_data, periode_id)

            # Suppression des lignes existantes pour ce trimestre
            db.query(models.BulletinLine).filter(
                models.BulletinLine.student_id == student.id,
                models.BulletinLine.trimestre == trimestre,
            ).delete()

            # Ligne de synthèse générale (bilan du PP)
            db.add(models.BulletinLine(
                id=str(uuid.uuid4()),
                student_id=student.id,
                trimestre=trimestre,
                subject="BILAN",
                appreciation=em.get("appreciationPP") or None,
                average=_parse_moyenne(em.get("moyenneGenerale")),
                absences=absences_total,
                tardiness=retards_total,
            ))

            # Une ligne par matière
            for disc in em.get("disciplines", []):
                db.add(models.BulletinLine(
                    id=str(uuid.uuid4()),
                    student_id=student.id,
                    trimestre=trimestre,
                    subject=disc.get("discipline", disc.get("codeMatiere", "")),
                    appreciation=disc.get("appreciationProfesseur") or None,
                    average=_parse_moyenne(disc.get("moyenne")),
                    absences=None,
                    tardiness=None,
                ))

            db.commit()

        except EcoleDirecteError as e:
            job.errors.append(f"{student.last_name} {student.first_name} : {e}")
        except Exception as e:
            job.errors.append(f"{student.last_name} {student.first_name} : erreur inattendue — {e}")
        finally:
            job.progress += 1
            time.sleep(0.5)  # ne pas surcharger EcoleDirecte

    client.close()
    db.close()
    job.status = "done"


def _parse_moyenne(value: str) -> float:
    """Convertit '14,69' ou '14.69' en float, retourne None si invalide."""
    if not value:
        return None
    try:
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return None


def _count_absences(vs_data: dict, periode_id: str) -> int:
    """Compte les demi-journées d'absence sur la période."""
    absences = vs_data.get("absences", [])
    return sum(
        1 for a in absences
        if a.get("idPeriode") == periode_id or not a.get("idPeriode")
    )


def _count_retards(vs_data: dict, periode_id: str) -> int:
    """Compte les retards sur la période."""
    retards = vs_data.get("retards", [])
    return sum(
        1 for r in retards
        if r.get("idPeriode") == periode_id or not r.get("idPeriode")
    )


@router.post("/fetch/{classe_id}", response_model=schemas.JobStatus)
def start_fetch(
    classe_id: str,
    trimestre: int,
    background_tasks: BackgroundTasks,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """
    Lance la récupération des bulletins d'une classe via l'API EcoleDirecte (background).
    Retourne un job_id pour suivre la progression via GET /jobs/{job_id}.
    """
    classe = db.query(models.Classe).filter(
        models.Classe.id == classe_id,
        models.Classe.teacher_id == teacher.id,
    ).first()
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    students = db.query(models.Student).filter(models.Student.classe_id == classe_id).all()
    if not students:
        raise HTTPException(
            status_code=400,
            detail="Aucun élève trouvé. Synchronisez d'abord les élèves.",
        )

    job_id = str(uuid.uuid4())
    _jobs[job_id] = schemas.JobStatus(
        job_id=job_id, status="running", progress=0, total=len(students), errors=[]
    )

    from database import DATABASE_URL
    background_tasks.add_task(
        _fetch_bulletins_job,
        job_id=job_id,
        ed_login=teacher.ecoledirecte_login,
        encrypted_password=teacher.encrypted_password,
        classe_id=classe_id,
        trimestre=trimestre,
        students=students,
        annee_scolaire=classe.annee_scolaire or "",
        db_url=DATABASE_URL,
    )
    return _jobs[job_id]


@router.get("/jobs/{job_id}", response_model=schemas.JobStatus)
def get_job_status(job_id: str):
    """Polling de la progression d'un job."""
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job introuvable")
    return job


@router.get("/{student_id}", response_model=List[schemas.BulletinLineOut])
def get_bulletin_lines(
    student_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """Retourne les lignes de bulletin d'un élève pour un trimestre."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")

    return (
        db.query(models.BulletinLine)
        .filter(
            models.BulletinLine.student_id == student_id,
            models.BulletinLine.trimestre == trimestre,
        )
        .all()
    )
