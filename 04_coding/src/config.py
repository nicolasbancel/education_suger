from pathlib import Path

BASE_DIR = Path("/Users/nicolasbancel/git/education_suger")


CONTRAINTES_PATH = BASE_DIR / "09_coding/templates/contraintes_physique.md"
PACKAGES_PATH = BASE_DIR / "mypackages.sty"
LATEX_TEMPLATE = BASE_DIR / "09_coding/templates/template_correction.tex"


ELEVES = {
    "3ème CI": [
        "Naël",
        "Faustine",
        "Isaure",
        "Lou",
        "Alina",
        "Charles",
        "Sadra",
        "Alexia",
        "Thais",
        "Valentine",
        "Kavya",
    ],
    "1ères STD2A": ["Milan", "Margaux", "Marjane", "Clem", "Katia", "Milena"],
}


for path in [CONTRAINTES_PATH, PACKAGES_PATH, LATEX_TEMPLATE]:
    if not path.exists():
        raise FileNotFoundError(f"Le chemin suivant est introuvable : {path}")
