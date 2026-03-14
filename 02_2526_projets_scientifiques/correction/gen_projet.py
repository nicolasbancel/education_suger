# -*- coding: utf-8 -*-
import json
import os
import re
import unicodedata
import subprocess


# -----------------------------
# Paramètres
# -----------------------------

TEMPLATE_FILE = "projet_template.tex"
JSON_FILE = "notes_enrichi.json"
OUTPUT_DIR = "evals_eleves"

# Mets à True si tu veux limiter aux 2 premiers élèves pour tester
ONLY_FIRST_TWO = True


# -----------------------------
# Mapping JSON -> commandes LaTeX
# -----------------------------

VAR_MAP = {
    "varPrenom": lambda e: e.get("prenom", ""),
    "varNom": lambda e: e.get("nom", ""),
    "varClasse": lambda e: e.get("classe", ""),
    "varAnticipationNote": lambda e: str(e.get("anticipation", {}).get("note", "")),
    "varAnticipationAppreciation": lambda e: e.get("anticipation", {}).get("appreciation", ""),
    "varInteractionNote": lambda e: str(e.get("interaction_teacher", {}).get("note", "")),
    "varInteractionAppreciation": lambda e: e.get("interaction_teacher", {}).get("appreciation", ""),
    "varAttitudeNote": lambda e: str(e.get("attitude_effort", {}).get("note", "")),
    "varAttitudeAppreciation": lambda e: e.get("attitude_effort", {}).get("appreciation", ""),
    "varFormulasNote": lambda e: str(e.get("formulas_sources", {}).get("note", "")),
    "varFormulasAppreciation": lambda e: e.get("formulas_sources", {}).get("appreciation", ""),
    "varNoteFinale": lambda e: str(e.get("note_finale", "")),
    "varAppreciationGenerale": lambda e: e.get("appreciation_generale", ""),
}


# -----------------------------
# Utilitaires
# -----------------------------


def slugify(text: str) -> str:
    nfkd_form = unicodedata.normalize("NFKD", text)
    no_accent = "".join(c for c in nfkd_form if not unicodedata.combining(c))
    s = no_accent.lower().replace(" ", "_")
    s = "".join(ch for ch in s if ch.isalnum() or ch == "_")
    return s


def replace_var(tex_content: str, var_name: str, value: str) -> str:
    """Remplace \\newcommand{\\varName}{...default...} par la vraie valeur."""
    pattern = re.compile(
        r"(\\newcommand\{\\" + re.escape(var_name) + r"\})\{.*?\}",
        re.DOTALL,
    )
    # Échapper les backslashes dans la valeur pour re.sub
    safe_value = value.replace("\\", "\\\\")
    return pattern.sub(r"\1{" + safe_value + "}", tex_content)


# -----------------------------
# Chargement du template et des données
# -----------------------------

with open(TEMPLATE_FILE, encoding="utf-8") as f:
    template_content = f.read()

with open(JSON_FILE, encoding="utf-8") as f:
    eleves = json.load(f)

if not isinstance(eleves, list):
    raise ValueError("Le fichier JSON doit contenir une liste d'élèves.")

if ONLY_FIRST_TWO:
    eleves = eleves[:2]

os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Génération + compilation
# -----------------------------

for eleve in eleves:
    prenom = eleve.get("prenom", "eleve")
    nom = eleve.get("nom", "")
    slug = slugify(f"{prenom}_{nom}")

    tex_filename = f"projet_{slug}.tex"
    pdf_filename = f"projet_{slug}.pdf"
    tex_path = os.path.join(OUTPUT_DIR, tex_filename)

    print(f"\n=== {prenom} {nom} ===")
    print(f"Génération de {tex_filename}...")

    # Remplacement des variables
    tex_content = template_content
    for var_name, extractor in VAR_MAP.items():
        tex_content = replace_var(tex_content, var_name, extractor(eleve))

    # Ajuster le chemin des packages (evals_eleves/ est un niveau plus bas)
    tex_content = tex_content.replace(
        "\\usepackage{../../", "\\usepackage{../../../"
    )

    with open(tex_path, "w", encoding="utf-8") as out:
        out.write(tex_content)

    # Compilation LaTeX -> PDF
    print(f"Compilation LaTeX vers PDF ({pdf_filename})...")

    try:
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
