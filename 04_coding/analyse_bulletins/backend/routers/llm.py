from __future__ import annotations
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from routers.auth import get_current_teacher
from services.llm_service import generate_student_output, get_default_generation_prompt

router = APIRouter(prefix="/api/llm", tags=["llm"])


@router.post("/generate", response_model=List[schemas.LLMOutputOut])
def generate(
    request: schemas.GenerateRequest,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """
    Génère les appréciations / synthèses / récompenses pour une liste d'élèves.
    Chaque élève doit avoir des BulletinLines en base pour le trimestre demandé.
    """
    results = []
    errors = []

    for student_id in request.student_ids:
        student = db.query(models.Student).filter(models.Student.id == student_id).first()
        if not student:
            errors.append(f"Élève {student_id} introuvable")
            continue

        lines = (
            db.query(models.BulletinLine)
            .filter(
                models.BulletinLine.student_id == student_id,
                models.BulletinLine.trimestre == request.trimestre,
            )
            .all()
        )
        if not lines:
            errors.append(
                f"{student.last_name} {student.first_name} : pas de données bulletin pour le trimestre {request.trimestre}"
            )
            continue

        lines_data = [
            {
                "matiere": l.subject,
                "appreciation": l.appreciation,
                "contenu": l.contenu,
                "moyenne": l.average,
                "moyenne_classe": l.average_class,
                "rang": l.rang,
                "absences": l.absences,
                "retards": l.tardiness,
            }
            for l in lines
        ]

        # Données du trimestre précédent (pour analyser l'évolution)
        prev_data = None
        if request.trimestre > 1:
            prev_t = request.trimestre - 1
            prev_lines = (
                db.query(models.BulletinLine)
                .filter(
                    models.BulletinLine.student_id == student_id,
                    models.BulletinLine.trimestre == prev_t,
                )
                .all()
            )
            prev_llm = (
                db.query(models.LLMOutput)
                .filter(
                    models.LLMOutput.student_id == student_id,
                    models.LLMOutput.trimestre == prev_t,
                )
                .first()
            )
            if prev_lines:
                prev_bilan = next((l for l in prev_lines if l.subject == "BILAN"), None)
                prev_data = {
                    "trimestre": prev_t,
                    "mention": prev_bilan.mention if prev_bilan else None,
                    "appreciation_generale": prev_llm.general_appreciation if prev_llm else None,
                    "lines": [
                        {
                            "matiere": l.subject,
                            "moyenne": l.average,
                            "appreciation": l.appreciation,
                        }
                        for l in prev_lines if l.subject != "BILAN"
                    ],
                }

        try:
            output = generate_student_output(
                prenom=student.first_name,
                nom=student.last_name,
                trimestre=request.trimestre,
                bulletin_lines=lines_data,
                custom_prompt=request.custom_prompt,
                prev_data=prev_data,
            )
        except Exception as e:
            errors.append(f"{student.last_name} {student.first_name} : LLM error — {e}")
            continue

        # Upsert LLMOutput
        existing = (
            db.query(models.LLMOutput)
            .filter(
                models.LLMOutput.student_id == student_id,
                models.LLMOutput.trimestre == request.trimestre,
            )
            .first()
        )
        if existing:
            db_output = existing
        else:
            db_output = models.LLMOutput(
                id=str(uuid.uuid4()),
                student_id=student_id,
                trimestre=request.trimestre,
            )
            db.add(db_output)

        db_output.general_appreciation = output["general_appreciation"]
        db_output.synthesis = output["synthesis"]
        db_output.reward_suggestion = output["reward_suggestion"]
        db_output.prompt_used = request.custom_prompt or get_default_generation_prompt()
        db_output.manually_edited = False
        db.commit()
        db.refresh(db_output)
        results.append(db_output)

    if errors and not results:
        raise HTTPException(status_code=422, detail=errors)

    return results


@router.patch("/outputs/{output_id}", response_model=schemas.LLMOutputOut)
def update_output(
    output_id: str,
    update: schemas.LLMOutputUpdate,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """Modification manuelle d'une sortie LLM par le professeur."""
    output = db.query(models.LLMOutput).filter(models.LLMOutput.id == output_id).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output introuvable")

    if update.general_appreciation is not None:
        output.general_appreciation = update.general_appreciation
    if update.synthesis is not None:
        output.synthesis = update.synthesis
    if update.reward_suggestion is not None:
        output.reward_suggestion = update.reward_suggestion
    output.manually_edited = True
    db.commit()
    db.refresh(output)
    return output


@router.get("/outputs/{classe_id}", response_model=List[schemas.StudentWithData])
def get_class_results(
    classe_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """Retourne les données complètes (bulletin + LLM) de tous les élèves d'une classe."""
    classe = db.query(models.Classe).filter(
        models.Classe.id == classe_id,
        models.Classe.teacher_id == teacher.id,
    ).first()
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    students = db.query(models.Student).filter(models.Student.classe_id == classe_id).all()
    results = []
    for s in students:
        lines = (
            db.query(models.BulletinLine)
            .filter(
                models.BulletinLine.student_id == s.id,
                models.BulletinLine.trimestre == trimestre,
            )
            .all()
        )
        llm_out = (
            db.query(models.LLMOutput)
            .filter(
                models.LLMOutput.student_id == s.id,
                models.LLMOutput.trimestre == trimestre,
            )
            .first()
        )
        results.append(
            schemas.StudentWithData(
                student=s,
                bulletin_lines=lines,
                llm_output=llm_out,
            )
        )
    return results


@router.get("/default-prompt")
def get_prompt():
    """Retourne le prompt par défaut de génération (pour affichage dans l'UI)."""
    return {"prompt": get_default_generation_prompt()}
