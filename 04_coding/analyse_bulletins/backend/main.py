from __future__ import annotations
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import engine, Base
import models  # noqa: F401 — nécessaire pour que SQLAlchemy crée les tables
from routers import auth, ecoledirecte, bulletins, llm, export

# Création des tables au démarrage
Base.metadata.create_all(bind=engine)

# Création du répertoire de données
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Bulletins API",
    description="API d'aide à la préparation des conseils de classe",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ecoledirecte.router)
app.include_router(bulletins.router)
app.include_router(llm.router)
app.include_router(export.router)


@app.get("/health")
def health():
    return {"status": "ok"}
