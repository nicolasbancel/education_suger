from __future__ import annotations
"""
Routes pour la récupération des données de bulletins via l'API EcoleDirecte.
Les données (notes, appréciations, vie scolaire) sont récupérées directement
en JSON — plus de téléchargement PDF ni d'extraction LLM factuelle.
La tâche tourne en background avec suivi de progression.
"""
import uuid
import time
import base64
import re
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from routers.auth import get_current_teacher
from services.ecoledirecte_client import EcoleDirecteClient, EcoleDirecteError
from services.crypto import decrypt
from config import TRIMESTRES_DATES

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

            # Récupération vie scolaire (absences/retards/sanctions)
            vs_data = client.get_student_vie_scolaire(token, eleve_id)
            absences_total = _count_absences(vs_data, trimestre)
            retards_total = _count_retards(vs_data, trimestre)

            # Suppression des lignes existantes pour ce trimestre
            db.query(models.BulletinLine).filter(
                models.BulletinLine.student_id == student.id,
                models.BulletinLine.trimestre == trimestre,
            ).delete()

            # Mise à jour des événements vie scolaire (toute l'année, pas par trimestre)
            db.query(models.VieScolaireEvent).filter(
                models.VieScolaireEvent.student_id == student.id,
            ).delete()
            for evt in vs_data.get("absencesRetards", []):
                db.add(models.VieScolaireEvent(
                    id=str(uuid.uuid4()),
                    student_id=student.id,
                    ed_id=evt.get("id"),
                    event_type=_classify_vie_scolaire(evt.get("libelle", "")),
                    date=evt.get("date"),
                    display_date=evt.get("displayDate"),
                    libelle=evt.get("libelle"),
                    motif=evt.get("motif"),
                    justifie=evt.get("justifie"),
                    commentaire=evt.get("commentaire"),
                ))

            db.query(models.SanctionEncouragement).filter(
                models.SanctionEncouragement.student_id == student.id,
            ).delete()
            for sanc in vs_data.get("sanctionsEncouragements", []):
                db.add(models.SanctionEncouragement(
                    id=str(uuid.uuid4()),
                    student_id=student.id,
                    ed_id=sanc.get("id"),
                    type_element=sanc.get("typeElement"),
                    date=sanc.get("date"),
                    display_date=sanc.get("displayDate"),
                    libelle=sanc.get("libelle"),
                    motif=sanc.get("motif"),
                    commentaire=sanc.get("commentaire"),
                ))

            # Ligne de synthèse générale (bilan du PP)
            # Les noms de champs EcoleDirecte pour le bilan conseil de classe :
            # mention       → "mention" ou "libelleMention"
            # appreciation_vs → "appreciationVS" (CPE)
            # appreciation_ce → "appreciationChefEtab" ou "appreciationEtablissement"
            mention = em.get("decisionDuConseil") or None
            appreciation_vs = em.get("appreciationVS") or None
            appreciation_ce = em.get("appreciationCE") or None
            db.add(models.BulletinLine(
                id=str(uuid.uuid4()),
                student_id=student.id,
                trimestre=trimestre,
                subject="BILAN",
                appreciation=em.get("appreciationPP") or None,
                average=_parse_moyenne(em.get("moyenneGenerale")),
                average_class=_parse_moyenne(em.get("moyenneClasse")),
                average_min=_parse_moyenne(em.get("moyenneMin")),
                average_max=_parse_moyenne(em.get("moyenneMax")),
                absences=absences_total,
                tardiness=retards_total,
                mention=mention,
                appreciation_vs=appreciation_vs,
                appreciation_ce=appreciation_ce,
            ))

            # Une ligne par matière
            for disc in em.get("disciplines", []):
                # Les appréciations sont dans disc["appreciations"] encodées en base64
                # appreciations[0] = appréciation du prof
                # appreciations[1] = contenus/éléments travaillés
                raw_apprs = disc.get("appreciations", [])
                appreciation = _decode_b64(raw_apprs[0]) if len(raw_apprs) > 0 else None
                contenu = _decode_b64(raw_apprs[1]) if len(raw_apprs) > 1 else None

                db.add(models.BulletinLine(
                    id=str(uuid.uuid4()),
                    student_id=student.id,
                    trimestre=trimestre,
                    subject=disc.get("discipline", disc.get("codeMatiere", "")),
                    appreciation=appreciation,
                    average=_parse_moyenne(disc.get("moyenne")),
                    average_class=_parse_moyenne(disc.get("moyenneClasse")),
                    average_min=_parse_moyenne(disc.get("moyenneMin")),
                    average_max=_parse_moyenne(disc.get("moyenneMax")),
                    rang=disc.get("rang"),
                    contenu=contenu,
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


def _decode_b64(value: str) -> str:
    """Décode une chaîne base64 EcoleDirecte en texte UTF-8."""
    if not value:
        return None
    try:
        return base64.b64decode(value).decode("utf-8").strip() or None
    except Exception:
        return value.strip() or None


def _parse_moyenne(value: str) -> float:
    """Convertit '14,69' ou '14.69' en float, retourne None si invalide."""
    if not value:
        return None
    try:
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return None


def _classify_vie_scolaire(libelle: str) -> str:
    """Classifie un événement : 'retard' si durée courte, 'absence' sinon.
    Reconnaît : '15 minutes', '00:15' (format HH:MM), '0:15'.
    """
    if not libelle:
        return "absence"
    lb = libelle.strip().lower()
    if "minute" in lb:
        return "retard"
    # Format HH:MM ou H:MM (ex: "00:15", "0:30")
    if re.match(r'^\d{1,2}:\d{2}$', lb):
        return "retard"
    return "absence"


def _date_in_trimestre(date_str: Optional[str], trimestre: int) -> bool:
    """Retourne True si la date est dans la plage du trimestre (config.py)."""
    if not date_str:
        return True  # pas de date → on inclut par défaut
    dates = TRIMESTRES_DATES.get(trimestre, {})
    debut = dates.get("debut", "")
    fin = dates.get("fin", "9999-12-31")
    return debut <= date_str <= fin


def _count_absences(vs_data: dict, trimestre: int) -> int:
    """Compte les absences (non-retards) dans absencesRetards, filtrées sur le trimestre."""
    events = vs_data.get("absencesRetards", [])
    return sum(
        1 for e in events
        if _classify_vie_scolaire(e.get("libelle", "")) == "absence"
        and _date_in_trimestre(e.get("date"), trimestre)
    )


def _count_retards(vs_data: dict, trimestre: int) -> int:
    """Compte les retards (libelle en minutes) dans absencesRetards, filtrés sur le trimestre."""
    events = vs_data.get("absencesRetards", [])
    return sum(
        1 for e in events
        if _classify_vie_scolaire(e.get("libelle", "")) == "retard"
        and _date_in_trimestre(e.get("date"), trimestre)
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


@router.get("/vie-scolaire/{student_id}", response_model=List[schemas.VieScolaireEventOut])
def get_vie_scolaire(
    student_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """Retourne les événements vie scolaire (absences/retards) d'un élève pour un trimestre."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    dates = TRIMESTRES_DATES.get(trimestre, {})
    debut = dates.get("debut", "")
    fin = dates.get("fin", "9999-12-31")
    return (
        db.query(models.VieScolaireEvent)
        .filter(
            models.VieScolaireEvent.student_id == student_id,
            models.VieScolaireEvent.date >= debut,
            models.VieScolaireEvent.date <= fin,
        )
        .order_by(models.VieScolaireEvent.date)
        .all()
    )


@router.get("/sanctions/{student_id}", response_model=List[schemas.SanctionEncouragementOut])
def get_sanctions(
    student_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """Retourne les sanctions/encouragements d'un élève pour un trimestre."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    dates = TRIMESTRES_DATES.get(trimestre, {})
    debut = dates.get("debut", "")
    fin = dates.get("fin", "9999-12-31")
    return (
        db.query(models.SanctionEncouragement)
        .filter(
            models.SanctionEncouragement.student_id == student_id,
            models.SanctionEncouragement.date >= debut,
            models.SanctionEncouragement.date <= fin,
        )
        .order_by(models.SanctionEncouragement.date)
        .all()
    )
