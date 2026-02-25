from __future__ import annotations
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, LargeBinary, Text
from sqlalchemy.sql import func
from database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(String, primary_key=True, default=gen_uuid)
    ecoledirecte_login = Column(String, nullable=False, unique=True)
    encrypted_password = Column(LargeBinary, nullable=False)
    # EcoleDirecte internal account ID (récupéré au login)
    ed_account_id = Column(Integer, nullable=True)
    session_token = Column(String, unique=True)
    created_at = Column(DateTime, server_default=func.now())


class Classe(Base):
    __tablename__ = "classes"
    id = Column(String, primary_key=True, default=gen_uuid)
    teacher_id = Column(String, ForeignKey("teachers.id"))
    name = Column(String)          # ex: "3ème B"
    ecoledirecte_id = Column(String)
    annee_scolaire = Column(String)  # ex: "2024-2025"


class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True, default=gen_uuid)
    classe_id = Column(String, ForeignKey("classes.id"))
    first_name = Column(String)
    last_name = Column(String)
    ecoledirecte_id = Column(String)


class BulletinLine(Base):
    """Une ligne par matière par élève par trimestre."""
    __tablename__ = "bulletin_lines"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    trimestre = Column(Integer)
    subject = Column(String)
    appreciation = Column(Text, nullable=True)   # appréciation du prof (décodée base64)
    contenu = Column(Text, nullable=True)         # éléments travaillés (décodés base64)
    average = Column(Float, nullable=True)
    average_class = Column(Float, nullable=True)
    average_min = Column(Float, nullable=True)
    average_max = Column(Float, nullable=True)
    rang = Column(Integer, nullable=True)
    absences = Column(Integer, nullable=True)
    tardiness = Column(Integer, nullable=True)
    # Champs spécifiques à la ligne BILAN (après conseil de classe)
    mention = Column(String, nullable=True)          # mention du conseil
    appreciation_vs = Column(Text, nullable=True)    # appréciation vie scolaire (CPE)
    appreciation_ce = Column(Text, nullable=True)    # appréciation chef d'établissement
    extracted_at = Column(DateTime, server_default=func.now())


class LLMOutput(Base):
    __tablename__ = "llm_outputs"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    trimestre = Column(Integer)
    general_appreciation = Column(Text, nullable=True)
    synthesis = Column(Text, nullable=True)
    reward_suggestion = Column(String, nullable=True)
    prompt_used = Column(Text, nullable=True)
    generated_at = Column(DateTime, server_default=func.now())
    manually_edited = Column(Boolean, default=False)


class VieScolaireEvent(Base):
    """Absence ou retard d'un élève (issu de viescolaire.awp → absencesRetards)."""
    __tablename__ = "vie_scolaire_events"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    ed_id = Column(Integer, nullable=True)        # id EcoleDirecte
    event_type = Column(String)                   # "absence" ou "retard"
    date = Column(String, nullable=True)          # "2026-03-18"
    display_date = Column(String, nullable=True)  # texte lisible EcoleDirecte
    libelle = Column(String, nullable=True)       # "1 demi-journée" / "30 minutes"
    motif = Column(String, nullable=True)
    justifie = Column(Boolean, nullable=True)
    commentaire = Column(Text, nullable=True)
    fetched_at = Column(DateTime, server_default=func.now())


class SanctionEncouragement(Base):
    """Sanction, punition ou encouragement d'un élève (viescolaire.awp → sanctionsEncouragements)."""
    __tablename__ = "sanctions_encouragements"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    ed_id = Column(Integer, nullable=True)
    type_element = Column(String, nullable=True)   # type fourni par EcoleDirecte
    date = Column(String, nullable=True)
    display_date = Column(String, nullable=True)
    libelle = Column(String, nullable=True)
    motif = Column(String, nullable=True)
    commentaire = Column(Text, nullable=True)
    fetched_at = Column(DateTime, server_default=func.now())
