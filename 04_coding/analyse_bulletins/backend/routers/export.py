"""
Export des résultats : CSV, DOCX, PDF.
"""
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
import models
from routers.auth import get_current_teacher
import pandas as pd
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

router = APIRouter(prefix="/api/export", tags=["export"])


def _get_class_data(
    classe_id: str, trimestre: int, teacher: models.Teacher, db: Session
) -> tuple[models.Classe, list[dict]]:
    classe = db.query(models.Classe).filter(
        models.Classe.id == classe_id,
        models.Classe.teacher_id == teacher.id,
    ).first()
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    students = db.query(models.Student).filter(models.Student.classe_id == classe_id).all()
    rows = []
    for s in students:
        output = (
            db.query(models.LLMOutput)
            .filter(
                models.LLMOutput.student_id == s.id,
                models.LLMOutput.trimestre == trimestre,
            )
            .first()
        )
        rows.append(
            {
                "Nom": s.last_name,
                "Prénom": s.first_name,
                "Appréciation générale": output.general_appreciation if output else "",
                "Synthèse": output.synthesis if output else "",
                "Récompense suggérée": output.reward_suggestion if output else "",
                "Modifié manuellement": output.manually_edited if output else False,
            }
        )
    return classe, rows


@router.get("/{classe_id}/csv")
def export_csv(
    classe_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    classe, rows = _get_class_data(classe_id, trimestre, teacher, db)
    df = pd.DataFrame(rows)
    buf = io.StringIO()
    df.to_csv(buf, index=False, encoding="utf-8-sig")
    buf.seek(0)
    filename = f"{classe.name}_T{trimestre}_resultats.csv".replace(" ", "_")
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{classe_id}/docx")
def export_docx(
    classe_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    classe, rows = _get_class_data(classe_id, trimestre, teacher, db)
    doc = Document()
    doc.add_heading(f"{classe.name} — Trimestre {trimestre}", 0)

    for row in rows:
        doc.add_heading(f"{row['Nom']} {row['Prénom']}", level=2)
        doc.add_paragraph(f"Appréciation générale :\n{row['Appréciation générale']}")
        doc.add_paragraph(f"Synthèse :\n{row['Synthèse']}")
        doc.add_paragraph(f"Récompense : {row['Récompense suggérée']}")
        doc.add_paragraph("")

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    filename = f"{classe.name}_T{trimestre}_resultats.docx".replace(" ", "_")
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{classe_id}/pdf")
def export_pdf(
    classe_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    classe, rows = _get_class_data(classe_id, trimestre, teacher, db)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"{classe.name} — Trimestre {trimestre}", styles["Title"]))
    story.append(Spacer(1, 12))

    for row in rows:
        story.append(Paragraph(f"<b>{row['Nom']} {row['Prénom']}</b>", styles["Heading2"]))
        story.append(Paragraph(f"<b>Appréciation :</b> {row['Appréciation générale']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Synthèse :</b> {row['Synthèse']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Récompense :</b> {row['Récompense suggérée']}", styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)
    buf.seek(0)
    filename = f"{classe.name}_T{trimestre}_resultats.pdf".replace(" ", "_")
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
