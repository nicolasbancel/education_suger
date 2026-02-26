# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Application d'aide à la préparation des conseils de classe** — web app that automates school class council preparation for French teachers using EcoleDirecte (https://www.ecoledirecte.com/).

For each student, it generates:
1. A general trimester assessment (based on teacher comments and grades)
2. A quick synthesis (strengths, areas for improvement, alerts)
3. A reward suggestion (félicitations, tableau d'honneur, encouragements, etc.)

**Scale**: ~1 teacher → ~4 classes → ~25 students → ~100 students/user.

## Stack

- **Backend**: FastAPI (Python 3.8) + SQLAlchemy + SQLite
- **Frontend**: Next.js 14 (App Router) + Tailwind CSS + TypeScript
- **LLM**: OpenAI GPT-4o via `openai` SDK (`OPENAI_API_KEY` in `.env`)
- **EcoleDirecte**: `httpx` client against reverse-engineered API (no official public API)
- **Encryption**: `cryptography` (Fernet) for EcoleDirecte credentials at rest

## Development Commands

### Setup (first time)

```bash
# Backend
cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp backend/.env.example backend/.env   # fill in OPENAI_API_KEY and SECRET_KEY

# Frontend
cd frontend && npm install
```

### Run

```bash
# Terminal 1 — backend (API + auto-reload)
cd backend && .venv/bin/uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev
```

- Backend API docs: http://localhost:8000/docs (Swagger UI)
- Frontend: http://localhost:3000

## Project Structure

```
backend/
├── main.py                    # FastAPI app entry point, table creation, CORS
├── database.py                # SQLAlchemy engine + get_db dependency
├── config.py                  # Trimestre date ranges (edit here to filter vie scolaire)
├── models.py                  # SQLAlchemy ORM models
├── schemas.py                 # Pydantic request/response schemas
├── routers/
│   ├── auth.py                # Login + get_current_teacher dependency
│   ├── ecoledirecte.py        # Sync classes/students from EcoleDirecte
│   ├── bulletins.py           # Fetch bulletins via notes.awp + viescolaire.awp (background job)
│   ├── llm.py                 # Generate + edit LLM outputs, class results view
│   └── export.py              # CSV / DOCX / PDF export
└── services/
    ├── crypto.py              # Fernet encrypt/decrypt for credentials
    ├── ecoledirecte_client.py # HTTP client for EcoleDirecte API
    └── llm_service.py         # OpenAI GPT-4o calls (generation mode)

frontend/
├── next.config.js             # Rewrites /api/* → localhost:8000/api/*
└── app/
    ├── page.tsx               # Login (EcoleDirecte credentials)
    ├── classes/page.tsx       # Class list + trimestre selection
    └── results/[classeId]/page.tsx  # Results view, edit, export
```

## Architecture Notes

### Auth flow
Teacher logs in with EcoleDirecte credentials → backend verifies against ED API → stores encrypted credentials (Fernet) in SQLite → returns `session_token` (UUID) → frontend stores in `localStorage` → sent as `Authorization: Bearer <token>` header.

### EcoleDirecte integration (validé 2025/2026)

Two distinct domains:
- **Auth only**: `https://api.ecoledirecte.com/v3`
- **All data**: `https://apip.ecoledirecte.com/v3`

Auth flow (2 steps):
1. GET `api.ecoledirecte.com/v3/login.awp?gtk=1&v=4.96.1` → reads cookie `GTK` (uppercase)
2. POST `api.ecoledirecte.com/v3/login.awp?v=4.96.1` with header `X-GTK` + credentials

Body format for all POST requests: `data=<url-encoded compact JSON>` (Content-Type: `application/x-www-form-urlencoded`)

Validated endpoints:
- Students of a class: `POST apip./v3/classes/{ecoledirecte_id}/eleves.awp?verbe=get`
- Notes/bulletins: `POST apip./v3/eleves/{id}/notes.awp?verbe=get` body: `data={"anneeScolaire":""}`
- Vie scolaire: `POST apip./v3/eleves/{id}/viescolaire.awp?verbe=get` body: `data={}`
- **Teacher's classes**: NOT a separate endpoint — come from `account.profile.classes` in login response

Known teacher account: `typeCompte="P"`, `id=123`, classes: 6EME (id=4), 5EME groupe mixte (id=3)

**Error 2406** (`L'objet n'est pas utilisable...`): EcoleDirecte server-side error that occurs when running direct login scripts while the backend server is running (or immediately after). Wait and retry, or stop the backend first.

### Data model — key fields

**`BulletinLine`** — one row per subject per student per trimester, plus one `subject="BILAN"` row:
- Subject rows: `average`, `average_class`, `average_min`, `average_max`, `appreciation` (base64-decoded), `contenu` (base64-decoded)
- BILAN row: `average` (moyenneGenerale), `average_class`, `average_min`, `average_max`, `absences`, `tardiness`, `appreciation` (appreciationPP), `mention` (decisionDuConseil), `appreciation_vs`, `appreciation_ce`

**`VieScolaireEvent`** — absences and retards from `viescolaire.awp → absencesRetards`:
- `event_type`: `"absence"` or `"retard"` — classified by `libelle`: `HH:MM` format or contains "minute" → retard, else → absence
- Stored for the whole school year; filtered by trimestre dates from `config.py` at query time

**`SanctionEncouragement`** — from `viescolaire.awp → sanctionsEncouragements`

### EcoleDirecte field names (ensembleMatieres)
- `appreciationPP` → PP appreciation
- `decisionDuConseil` → mention (Félicitations, Tableau d'honneur, Encouragements, etc.)
- `appreciationVS` → vie scolaire (CPE) appreciation
- `appreciationCE` → chef d'établissement appreciation
- `moyenneGenerale`, `moyenneClasse`, `moyenneMin`, `moyenneMax`
- Appreciations in `disciplines[].appreciations[]` are **base64-encoded**: index 0 = teacher appreciation, index 1 = topics covered (`contenu`)

### LLM generation pipeline
- Model: `gpt-4o` (OpenAI)
- `generate_student_output()` in `llm_service.py` builds a structured prompt with:
  - Current trimester: per-subject average, class average, appreciation, contenu, absences/retards
  - Previous trimester (if T>1): per-subject evolution with delta, previous mention, previous general appreciation
- Frontend sends students in **batches of 5** to avoid browser timeout (~2 min for 25 students)

### Background jobs
Bulletin fetch runs in a FastAPI `BackgroundTask`. Progress tracked in `_jobs` dict (in-memory). Frontend polls `GET /api/bulletins/jobs/{job_id}` every 2 seconds.

### Trimestre date configuration
Edit `backend/config.py` to set start/end dates per trimester. Used to filter `VieScolaireEvent` and `SanctionEncouragement` queries, and to count absences/retards in the BILAN row.

```python
TRIMESTRES_DATES = {
    1: {"debut": "2025-09-02", "fin": "2025-12-19"},
    2: {"debut": "2026-01-05", "fin": "2026-03-27"},
    3: {"debut": "2026-04-06", "fin": "2026-07-04"},
}
```

## Key Domain Concepts

- **Bulletin**: school report for one student for one trimester (fetched via JSON API, not PDF)
- **Conseil de classe**: quarterly class council meeting — populates `decisionDuConseil`, `appreciationCE`, `appreciationVS`
- **Professeur principal**: head teacher who prepares summaries for all students
- **EcoleDirecte**: French school management SaaS
- `idPeriode`: ED internal period ID — `"A001"` = trimestre 1, `"A002"` = T2, `"A003"` = T3

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key (GPT-4o) |
| `ANTHROPIC_API_KEY` | Legacy — no longer used for generation |
| `SECRET_KEY` | Random string used to derive Fernet encryption key |
| `DATABASE_URL` | SQLite path (default: `sqlite:///./bulletins.db`) |
| `DATA_DIR` | Where PDFs are stored (default: `./data`) |

## Python 3.8 compatibility

- Always `from __future__ import annotations` at the top of every backend file
- Use `Optional[str]`, `List[dict]`, `Tuple[...]` — not `str | None`, `list[dict]`
- `response_model=List[...]` in FastAPI decorators
