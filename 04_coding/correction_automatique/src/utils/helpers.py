import datetime
import os
import re
import base64
import json
from pathlib import Path


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def get_date_format_francais():
    mois_fr = {
        1: "Janvier",
        2: "Février",
        3: "Mars",
        4: "Avril",
        5: "Mai",
        6: "Juin",
        7: "Juillet",
        8: "Août",
        9: "Septembre",
        10: "Octobre",
        11: "Novembre",
        12: "Décembre",
    }

    aujourd_hui = datetime.date.today()
    date_francais = f"{aujourd_hui.day} {mois_fr[aujourd_hui.month]} {aujourd_hui.year}"
    return date_francais


def extract_class_and_subject_from_path(full_path: str):
    """
    Extrait la classe et la matière à partir d'un chemin complet.
    Il cherche dans les dossiers du chemin un nom du type '00_1ères_STD2A_maths'.
    """
    matiere_map = {
        "pc": "Physique-Chimie",
        "maths": "Maths",
        "svt": "SVT",
        "fr": "Français",
        "hg": "Histoire-Géo",
    }

    # On découpe chaque dossier du chemin
    parts = full_path.split(os.sep)

    # On cherche le dossier qui matche le motif attendu
    pattern = re.compile(r"^\d{2}_.+_.+$")  # ex: 00_1ères_STD2A_maths

    for part in parts:
        if pattern.match(part):
            tokens = part.split("_")
            classe = " ".join(tokens[1:-1])
            matiere_code = tokens[-1].lower()
            matiere = matiere_map.get(matiere_code, matiere_code.capitalize())
            return classe, matiere

    raise ValueError(
        "Aucun dossier du chemin ne correspond au format attendu (ex: 00_1ères_STD2A_maths)"
    )


def get_image_files(folder_path):
    """
    Retourne une liste de chemins d’images (.jpg, .jpeg, .png) dans le dossier spécifié.
    """
    valid_extensions = (".jpg", ".jpeg", ".png")
    image_files = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            image_files.append(os.path.join(folder_path, filename))

    return image_files


def save_variable_to_json(variable, file_path):
    # Détermine le nom du fichier JSON de log
    base_path = Path(file_path)
    log_path = base_path.with_name(base_path.stem + "_logs.json")

    # Sauvegarde du contenu au format JSON lisible
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(variable, f, ensure_ascii=False, indent=2)

    print(f"✅ Fichier de log sauvegardé dans : {log_path}")


if __name__ == "__main__":
    pass
