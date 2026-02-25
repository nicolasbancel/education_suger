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

- **Backend**: FastAPI (Python 3.11) + SQLAlchemy + SQLite
- **Frontend**: Next.js 14 (App Router) + Tailwind CSS + TypeScript
- **LLM**: Claude API (`claude-sonnet-4-6`) via `anthropic` SDK
- **PDF extraction**: `pdfplumber` (primary) + `PyMuPDF` (fallback)
- **EcoleDirecte**: `httpx` client against reverse-engineered API (no official public API)
- **Encryption**: `cryptography` (Fernet) for EcoleDirecte credentials at rest

## Development Commands

### Setup (first time)

```bash
# Backend
cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp backend/.env.example backend/.env   # then fill in ANTHROPIC_API_KEY and SECRET_KEY

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

- Backend API docs: http://localhost:8000/docs (Swagger UI — use this to test in console)
- Frontend: http://localhost:3000

## Project Structure

```
backend/
├── main.py                    # FastAPI app entry point, table creation, CORS
├── database.py                # SQLAlchemy engine + get_db dependency
├── models.py                  # SQLAlchemy ORM models
├── schemas.py                 # Pydantic request/response schemas
├── routers/
│   ├── auth.py                # Login + get_current_teacher dependency
│   ├── ecoledirecte.py        # Sync classes/students from EcoleDirecte
│   ├── bulletins.py           # Download PDFs + background extraction job
│   ├── llm.py                 # Generate + edit LLM outputs, class results view
│   └── export.py              # CSV / DOCX / PDF export
└── services/
    ├── crypto.py              # Fernet encrypt/decrypt for credentials
    ├── ecoledirecte_client.py # HTTP client for EcoleDirecte API
    ├── pdf_extractor.py       # pdfplumber + PyMuPDF text extraction
    └── llm_service.py         # Claude API calls (extraction + generation modes)

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

### EcoleDirecte integration
- No official API — reverse-engineered endpoints at `https://api.ecoledirecte.com/v3/`
- `data=<urlencoded_json>` body format for all POST requests
- `X-Token` header for authenticated requests
- Login returns token + account list; teacher accounts have `typeCompte == "P"`
- **The bulletin PDF download endpoint is the most uncertain** — see `services/ecoledirecte_client.py` for notes and fallback logic. Check https://github.com/EduWireApps/ecoledirecte-api-docs if it breaks.

### LLM two-mode pipeline
- **Extraction mode** (`extract_bulletin_data`): strict JSON output, no interpretation, null for missing fields
- **Generation mode** (`generate_student_output`): teacher-configurable prompt, returns `{appreciation_generale, synthese, suggestion_recompense}`
- Default generation prompt exposed via `GET /api/llm/default-prompt` and editable in UI

### Background jobs
PDF download + LLM extraction runs in a FastAPI `BackgroundTask`. Progress tracked in `_jobs` dict (in-memory). Frontend polls `GET /api/bulletins/jobs/{job_id}` every 2 seconds.

### Data storage
- PDFs saved to `DATA_DIR/{teacher_id}/{classe_id}/trimestre_{n}/{student_id}.pdf`
- `DATA_DIR` defaults to `./data` (relative to `backend/`)
- **Never commit `backend/data/` or `backend/*.db`** — contains sensitive student data

## Key Domain Concepts

- **Bulletin**: PDF school report for one student for one trimester
- **Conseil de classe**: quarterly class council meeting
- **Professeur principal**: head teacher who prepares summaries for all students
- **EcoleDirecte**: French school management SaaS
- `idPeriode`: ED internal period ID — `"A001"` = trimestre 1, `"A002"` = T2, `"A003"` = T3

## Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API key |
| `SECRET_KEY` | Random string used to derive Fernet encryption key |
| `DATABASE_URL` | SQLite path (default: `sqlite:///./bulletins.db`) |
| `DATA_DIR` | Where PDFs are stored (default: `./data`) |
