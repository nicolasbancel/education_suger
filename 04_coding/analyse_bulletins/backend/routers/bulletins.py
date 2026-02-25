"""
Routes pour le téléchargement et l'extraction des bulletins PDF.
Le téléchargement tourne en background task avec suivi de progression.
"""
import os
import time
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from routers.auth import get_current_teacher
from services.ecoledirecte_client import EcoleDirecteClient, EcoleDirecteError
from services.crypto import decrypt
from services.pdf_extractor import extract_text_from_pdf
from services.llm_service import extract_bulletin_data

router = APIRouter(prefix="/api/bulletins", tags=["bulletins"])

# Suivi des jobs en mémoire (suffisant pour MVP local mono-utilisateur)
_jobs: dict[str, schemas.JobStatus] = {}

DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))


def _get_pdf_path(teacher_id: str, classe_id: str, trimestre: int, student_id: str) -> Path:
    folder = DATA_DIR / teacher_id / classe_id / f"trimestre_{trimestre}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{student_id}.pdf"


def _download_and_extract_job(
    job_id: str,
    teacher_id: str,
    ed_login: str,
    encrypted_password: bytes,
    classe_id: str,
    trimestre: int,
    students: list[models.Student],
    annee_scolaire: str,
    db_url: str,
):
    """Tâche de fond : télécharge les PDFs + extrait les données via LLM."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    db = Session()

    job = _jobs[job_id]
    job.total = len(students)

    password = decrypt(encrypted_password)
    client = EcoleDirecteClient()

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
            # Téléchargement PDF
            pdf_bytes = client.download_bulletin_pdf(
                token,
                int(student.ecoledirecte_id),
                trimestre,
                annee_scolaire,
            )
            pdf_path = _get_pdf_path(teacher_id, classe_id, trimestre, student.id)
            pdf_path.write_bytes(pdf_bytes)

            # Extraction texte
            text = extract_text_from_pdf(str(pdf_path))
            if not text:
                job.errors.append(
                    f"{student.last_name} {student.first_name} : PDF illisible (texte vide)"
                )
                job.progress += 1
                continue

            # Extraction LLM (mode factuel)
            lines = extract_bulletin_data(text)

            # Suppression des lignes existantes pour ce trimestre
            db.query(models.BulletinLine).filter(
                models.BulletinLine.student_id == student.id,
                models.BulletinLine.trimestre == trimestre,
            ).delete()

            for line in lines:
                db.add(
                    models.BulletinLine(
                        id=str(uuid.uuid4()),
                        student_id=student.id,
                        trimestre=trimestre,
                        subject=line.get("matiere", ""),
                        appreciation=line.get("appreciation"),
                        average=line.get("moyenne"),
                        absences=line.get("absences"),
                        tardiness=line.get("retards"),
                        pdf_path=str(pdf_path),
                    )
                )
            db.commit()

        except Exception as e:
            job.errors.append(
                f"{student.last_name} {student.first_name} : {e}"
            )
        finally:
            job.progress += 1
            # Délai pour ne pas surcharger EcoleDirecte
            time.sleep(1.0)

    client.close()
    db.close()
    job.status = "done"


@router.post("/download/{classe_id}", response_model=schemas.JobStatus)
def start_download(
    classe_id: str,
    trimestre: int,
    background_tasks: BackgroundTasks,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """
    Lance le téléchargement + extraction des bulletins d'une classe en arrière-plan.
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
            detail="Aucun élève trouvé. Synchronisez d'abord les élèves via /ecoledirecte/classes/{id}/sync-students",
        )

    job_id = str(uuid.uuid4())
    _jobs[job_id] = schemas.JobStatus(
        job_id=job_id, status="running", progress=0, total=len(students), errors=[]
    )

    from database import DATABASE_URL
    background_tasks.add_task(
        _download_and_extract_job,
        job_id=job_id,
        teacher_id=teacher.id,
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
    """Polling de la progression d'un job de téléchargement."""
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job introuvable")
    return job


@router.get("/{student_id}", response_model=list[schemas.BulletinLineOut])
def get_bulletin_lines(
    student_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """Retourne les lignes extraites du bulletin d'un élève."""
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
