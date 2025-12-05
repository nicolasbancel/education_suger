# -*- coding: utf-8 -*-
import json
import os
import unicodedata
import subprocess

from jinja2 import Environment, FileSystemLoader


# -----------------------------
# Paramètres
# -----------------------------

TEMPLATE_FILE = "tenue_cahier_template.tex"
JSON_FILE = "toutes_notes.json"
OUTPUT_DIR = "evals_eleves"

# Mets à True si tu veux limiter aux 2 premiers élèves pour tester
ONLY_FIRST_TWO = False


# -----------------------------
# Utilitaire : slug pour les noms de fichiers
# -----------------------------


def slugify_prenom(prenom: str) -> str:
    """
    Transforme un prénom en nom de fichier propre :
    - minuscules
    - accents supprimés
    - espaces -> underscores
    - caractères non alphanumériques supprimés
    """
    nfkd_form = unicodedata.normalize("NFKD", prenom)
    no_accent = "".join(c for c in nfkd_form if not unicodedata.combining(c))
    s = no_accent.lower()
    s = s.replace(" ", "_")
    s = "".join(ch for ch in s if ch.isalnum() or ch == "_")
    return s


# -----------------------------
# Préparation du moteur Jinja2
# -----------------------------
"""
env = Environment(
    loader=FileSystemLoader("."),
    autoescape=False,
    variable_start_string="(( ",
    variable_end_string=" ))",
    comment_start_string="((#",
    comment_end_string="#))",
)
"""

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=False,
    variable_start_string="[[",
    variable_end_string="]]",
    comment_start_string="[#",
    comment_end_string="#]",
)


template = env.get_template(TEMPLATE_FILE)

# Dossier de sortie
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Chargement des données JSON
# -----------------------------

with open(JSON_FILE, encoding="utf-8") as f:
    eleves = json.load(f)

if not isinstance(eleves, list):
    raise ValueError("Le fichier JSON doit contenir une liste d'élèves.")

if ONLY_FIRST_TWO:
    eleves = eleves[:2]


# -----------------------------
# Génération + compilation
# -----------------------------

for eleve in eleves:
    prenom = eleve.get("prenom", "eleve")
    slug = slugify_prenom(prenom)

    tex_filename = f"note_cahiers_{slug}.tex"
    pdf_filename = f"note_cahiers_{slug}.pdf"
    tex_path = os.path.join(OUTPUT_DIR, tex_filename)

    print(f"\n=== {prenom} ===")
    print(f"Génération de {tex_filename}...")

    # Rendu du template
    tex_content = template.render(**eleve)

    # Écriture du .tex
    with open(tex_path, "w", encoding="utf-8") as out:
        out.write(tex_content)

    # -------------------------
    # Compilation LaTeX -> PDF
    # -------------------------
    print(f"Compilation LaTeX vers PDF ({pdf_filename})...")

    try:
        # On lance pdflatex dans le dossier OUTPUT_DIR
        subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                tex_filename,
            ],
            cwd=OUTPUT_DIR,
            check=True,
        )
        # Si tu veux une 2e passe (souvent inutile ici), tu peux relancer pdflatex une 2e fois
        # subprocess.run(
        #     [
        #         "pdflatex",
        #         "-interaction=nonstopmode",
        #         "-halt-on-error",
        #         tex_filename,
        #     ],
        #     cwd=OUTPUT_DIR,
        #     check=True,
        # )

        print(f"✅ PDF généré : {pdf_filename}")

    except subprocess.CalledProcessError:
        print(f"❌ Erreur lors de la compilation de {tex_filename}.")
        print(
            "Vérifie les logs dans le fichier .log correspondant dans le dossier evals_eleves."
        )


print(
    "\n✅ Terminé : tous les fichiers .tex et .pdf ont été générés (ou tentés) dans",
    OUTPUT_DIR,
)
