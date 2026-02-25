from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List


# --- Auth ---

class LoginRequest(BaseModel):
    ecoledirecte_login: str
    ecoledirecte_password: str


class LoginResponse(BaseModel):
    session_token: str
    teacher_id: str


# --- EcoleDirecte ---

class ClasseOut(BaseModel):
    id: str
    name: str
    ecoledirecte_id: str
    annee_scolaire: str

    class Config:
        from_attributes = True


class StudentOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    ecoledirecte_id: str

    class Config:
        from_attributes = True


# --- Bulletins ---

class BulletinLineOut(BaseModel):
    id: str
    subject: str
    appreciation: Optional[str]
    contenu: Optional[str]
    average: Optional[float]
    average_class: Optional[float]
    average_min: Optional[float]
    average_max: Optional[float]
    rang: Optional[int]
    absences: Optional[int]
    tardiness: Optional[int]
    mention: Optional[str]
    appreciation_vs: Optional[str]
    appreciation_ce: Optional[str]

    class Config:
        from_attributes = True


# --- LLM ---

class LLMOutputOut(BaseModel):
    id: str
    general_appreciation: Optional[str]
    synthesis: Optional[str]
    reward_suggestion: Optional[str]
    prompt_used: Optional[str]
    manually_edited: bool

    class Config:
        from_attributes = True


class LLMOutputUpdate(BaseModel):
    general_appreciation: Optional[str] = None
    synthesis: Optional[str] = None
    reward_suggestion: Optional[str] = None


class GenerateRequest(BaseModel):
    student_ids: List[str]
    trimestre: int
    custom_prompt: Optional[str] = None


# --- Results ---

class StudentWithData(BaseModel):
    student: StudentOut
    bulletin_lines: List[BulletinLineOut]
    llm_output: Optional[LLMOutputOut]


# --- Vie scolaire ---

class VieScolaireEventOut(BaseModel):
    id: str
    event_type: str
    date: Optional[str]
    display_date: Optional[str]
    libelle: Optional[str]
    motif: Optional[str]
    justifie: Optional[bool]
    commentaire: Optional[str]

    class Config:
        from_attributes = True


class SanctionEncouragementOut(BaseModel):
    id: str
    type_element: Optional[str]
    date: Optional[str]
    display_date: Optional[str]
    libelle: Optional[str]
    motif: Optional[str]
    commentaire: Optional[str]

    class Config:
        from_attributes = True


# --- Jobs (background tasks) ---

class JobStatus(BaseModel):
    job_id: str
    status: str  # "running" | "done" | "error"
    progress: int
    total: int
    errors: List[str]
