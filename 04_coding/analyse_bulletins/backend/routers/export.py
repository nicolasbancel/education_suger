from __future__ import annotations
"""
Export des résultats : CSV, DOCX, PDF.
"""
import html as html_lib
import io
import re
from pathlib import Path
from typing import Tuple, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.orm import Session
from weasyprint import HTML as WeasyHTML
from database import get_db
import models
from routers.auth import get_current_teacher
from config import TRIMESTRES_DATES
import pandas as pd
from docx import Document

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_jinja_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)

router = APIRouter(prefix="/api/export", tags=["export"])


def _get_class_data(
    classe_id: str, trimestre: int, teacher: models.Teacher, db: Session
) -> Tuple[models.Classe, List[dict]]:
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


# ─── Helpers PDF ──────────────────────────────────────────────────────────────

def _fmt(val: Optional[float]) -> str:
    """Formate une moyenne en '14.36' ou '—' si absente."""
    if val is None:
        return "—"
    return f"{val:.2f}"


def _delta_str(delta: Optional[float]) -> str:
    """Formate un delta avec signe (+2.15 / -1.30 / —)."""
    if delta is None:
        return "—"
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.2f}"


def _delta_color_css(delta: Optional[float]) -> str:
    """
    Retourne une couleur CSS inline pour la cellule Δ :
    - négatif → rouge (plus intense si |Δ| grand)
    - positif → vert (plus intense si |Δ| grand)
    - None ou zéro → transparent
    Seuil de saturation maximale : |Δ| = 3 points.
    """
    if delta is None or delta == 0:
        return "transparent"
    intensity = min(abs(delta) / 3.0, 1.0)
    if delta < 0:
        r, g, b = 255, int(255 - 178 * intensity), int(255 - 178 * intensity)
    else:
        r, g, b = int(255 - 178 * intensity), 255, int(255 - 178 * intensity)
    return f"rgb({r},{g},{b})"


def _synthesis_to_html(synthesis: Optional[str]) -> str:
    """
    Convertit la synthèse structurée (Points forts / Axes d'amélioration / Alertes)
    en HTML avec labels en gras et listes à puces.
    """
    if not synthesis:
        return ""
    pattern = re.compile(r"(Points forts|Axes?\s+d.amélioration|Alertes?)\s*:", re.IGNORECASE)
    parts = pattern.split(synthesis.strip())

    if len(parts) <= 1:
        lines = [l.strip().lstrip("-•").strip() for l in synthesis.split("\n") if l.strip()]
        items = "".join(f"<li>{html_lib.escape(l)}</li>" for l in lines)
        return f"<ul>{items}</ul>" if items else html_lib.escape(synthesis.strip())

    result = []
    for i in range(1, len(parts) - 1, 2):
        label = html_lib.escape(parts[i].strip())
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        result.append(f'<p class="syn-label">{label} :</p>')
        bullets = [
            l.strip().lstrip("-•").strip()
            for l in re.split(r"\n|(?<=[.!?])\s+", content)
            if l.strip()
        ]
        if bullets:
            items = "".join(f"<li>{html_lib.escape(b)}</li>" for b in bullets)
            result.append(f"<ul>{items}</ul>")
    return "".join(result)


def _fmt_event(e: models.VieScolaireEvent) -> str:
    parts = [e.display_date or e.date or ""]
    if e.libelle:
        parts.append(e.libelle)
    if e.motif:
        parts.append(f"— {e.motif}")
    return " · ".join(p for p in parts if p)


def _fmt_sanction(s: models.SanctionEncouragement) -> str:
    parts = [s.display_date or s.date or ""]
    if s.type_element:
        parts.append(s.type_element)
    if s.libelle:
        parts.append(f"— {s.libelle}")
    if s.motif:
        parts.append(f"({s.motif})")
    return " · ".join(p for p in parts if p)


# ─── Export PDF ───────────────────────────────────────────────────────────────

@router.get("/{classe_id}/pdf")
def export_pdf(
    classe_id: str,
    trimestre: int,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """
    Génère un PDF par élève (HTML/CSS via WeasyPrint) avec :
    - Tableau de notes T_n vs T_{n-1} (gradient couleur sur le delta)
    - Bilan trimestre précédent (PP, mention, CE)
    - Incidents / Vie scolaire du trimestre
    - Appréciations LLM (général, synthèse, récompense)
    """
    classe = db.query(models.Classe).filter(
        models.Classe.id == classe_id,
        models.Classe.teacher_id == teacher.id,
    ).first()
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    students = db.query(models.Student).filter(models.Student.classe_id == classe_id).all()

    dates_tn = TRIMESTRES_DATES.get(trimestre, {})
    debut_tn = dates_tn.get("debut", "")
    fin_tn = dates_tn.get("fin", "9999-12-31")
    prev_t = trimestre - 1
    prev_label = f"T{prev_t}" if trimestre > 1 else "T0"

    students_ctx = []

    for student in students:
        lines_tn = (
            db.query(models.BulletinLine)
            .filter(
                models.BulletinLine.student_id == student.id,
                models.BulletinLine.trimestre == trimestre,
            )
            .all()
        )
        lines_prev = (
            db.query(models.BulletinLine)
            .filter(
                models.BulletinLine.student_id == student.id,
                models.BulletinLine.trimestre == prev_t,
            )
            .all()
        ) if trimestre > 1 else []

        bilan_tn = next((l for l in lines_tn if l.subject == "BILAN"), None)
        bilan_prev = next((l for l in lines_prev if l.subject == "BILAN"), None)
        subjects_tn = [l for l in lines_tn if l.subject != "BILAN"]
        prev_by_subject = {l.subject: l for l in lines_prev if l.subject != "BILAN"}

        llm = (
            db.query(models.LLMOutput)
            .filter(
                models.LLMOutput.student_id == student.id,
                models.LLMOutput.trimestre == trimestre,
            )
            .first()
        )

        vie_scolaire = (
            db.query(models.VieScolaireEvent)
            .filter(
                models.VieScolaireEvent.student_id == student.id,
                models.VieScolaireEvent.date >= debut_tn,
                models.VieScolaireEvent.date <= fin_tn,
            )
            .order_by(models.VieScolaireEvent.date)
            .all()
        )
        sanctions_list = (
            db.query(models.SanctionEncouragement)
            .filter(
                models.SanctionEncouragement.student_id == student.id,
                models.SanctionEncouragement.date >= debut_tn,
                models.SanctionEncouragement.date <= fin_tn,
            )
            .order_by(models.SanctionEncouragement.date)
            .all()
        )

        abs_non_just = [e for e in vie_scolaire if e.event_type == "absence" and e.justifie is False]
        retards = [e for e in vie_scolaire if e.event_type == "retard"]

        # ── Lignes matières ─────────────────────────────────────────────
        subjects_ctx = []
        for line in subjects_tn:
            prev_line = prev_by_subject.get(line.subject)
            avg_tn = line.average
            avg_prev = prev_line.average if prev_line else None
            delta = (avg_tn - avg_prev) if (avg_tn is not None and avg_prev is not None) else None
            subjects_ctx.append({
                "subject": line.subject,
                "avg_tn": _fmt(avg_tn),
                "avg_class": _fmt(line.average_class),
                "avg_prev": _fmt(avg_prev),
                "delta_str": _delta_str(delta),
                "delta_color": _delta_color_css(delta),
                "appreciation_tn": line.appreciation or "—",
                "appreciation_prev": (prev_line.appreciation or "—") if prev_line else "—",
            })

        # ── Ligne Moyenne générale ───────────────────────────────────────
        avg_tn_g = bilan_tn.average if bilan_tn else None
        avg_cls_g = bilan_tn.average_class if bilan_tn else None
        avg_prev_g = bilan_prev.average if bilan_prev else None
        delta_g = (
            (avg_tn_g - avg_prev_g)
            if (avg_tn_g is not None and avg_prev_g is not None)
            else None
        )
        bilan_ctx = {
            "avg_tn": _fmt(avg_tn_g),
            "avg_class": _fmt(avg_cls_g),
            "avg_prev": _fmt(avg_prev_g),
            "delta_str": _delta_str(delta_g),
            "delta_color": _delta_color_css(delta_g),
        }

        # ── LLM ─────────────────────────────────────────────────────────
        llm_ctx = None
        if llm:
            llm_ctx = {
                "general_appreciation": llm.general_appreciation,
                "synthesis_html": _synthesis_to_html(llm.synthesis),
                "reward_suggestion": llm.reward_suggestion,
            }

        students_ctx.append({
            "first_name": student.first_name,
            "last_name": student.last_name,
            "subjects": subjects_ctx,
            "bilan": bilan_ctx,
            "bilan_prev": bilan_prev is not None,
            "bilan_prev_appreciation": bilan_prev.appreciation if bilan_prev else None,
            "bilan_prev_mention": (bilan_prev.mention or "Pas de récompense / mention") if bilan_prev else "Pas de récompense / mention",
            "bilan_prev_ce": bilan_prev.appreciation_ce if bilan_prev else None,
            "abs_non_just": [_fmt_event(e) for e in abs_non_just],
            "retards": [_fmt_event(e) for e in retards],
            "sanctions": [_fmt_sanction(s) for s in sanctions_list],
            "llm": llm_ctx,
        })

    template = _jinja_env.get_template("bulletin.html")
    html_str = template.render(
        students=students_ctx,
        classe_name=classe.name,
        trimestre=trimestre,
        prev_label=prev_label,
    )

    buf = io.BytesIO()
    WeasyHTML(string=html_str).write_pdf(buf)
    buf.seek(0)

    filename = f"{classe.name}_T{trimestre}_resultats.pdf".replace(" ", "_")
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
