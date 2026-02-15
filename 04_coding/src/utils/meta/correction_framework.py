import os
import sys

src_path = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from utils.latex_parser import extract_exercises_from_latex
from utils.helpers import extract_class_and_subject_from_path
from config import ELEVES
import pandas as pd

FILE_PATH = (
    "/Users/nicolasbancel/git/education_suger/01_1ères_STD2A_pc/ds/interrogation_2.tex"
)
# "/Users/nicolasbancel/git/education_suger/02_3ème_CI_pc/ds/brevet_blanc_2.tex"


def generate_bareme(
    classe: str, exercices: list, eleves_par_classe: dict
) -> pd.DataFrame:
    """
    Génère un tableau DataFrame avec les colonnes :
    Partie, N° Question, Sous question, Barème, <élèves...>

    :param classe: Nom de la classe ("3ème CI", etc.)
    :param exercices: Liste des exercices au format JSON
    :param eleves_par_classe: Dictionnaire {classe: [élèves]}
    :return: DataFrame
    """
    if classe not in eleves_par_classe:
        raise ValueError(f"Classe '{classe}' non trouvée dans les données.")

    rows = []
    for exo in exercices:
        partie = f"Exercice {exo['numero_exercice']} – {exo['titre_exercice']}"
        for question in exo["questions_exercice"]:
            rows.append(
                {
                    "Partie": partie,
                    "N° Question": question["marker"],
                    "Sous question": "",  # À compléter si besoin
                    "Barème": question["points"],
                }
            )

    df = pd.DataFrame(rows)

    # Ajouter une colonne par élève, vide
    for eleve in eleves_par_classe[classe]:
        df[eleve] = ""

    return df


def exporter_bareme_csv(df: pd.DataFrame, path_latex: str) -> str:
    """
    Exporte un DataFrame de barème vers un fichier CSV, en se basant sur le
    chemin du fichier LaTeX d'origine. Le fichier CSV aura le suffixe "_bareme".

    :param df: DataFrame contenant le barème (avec élèves)
    :param path_latex: Chemin du fichier .tex initial
    :return: Chemin du fichier CSV généré
    """
    base, _ = os.path.splitext(path_latex)
    path_csv = base + "_bareme.csv"
    df.to_csv(path_csv, index=False)
    return path_csv


if __name__ == "__main__":

    exercices = extract_exercises_from_latex(FILE_PATH)
    classe, matiere = extract_class_and_subject_from_path(FILE_PATH)
    bareme = generate_bareme(classe, exercices, ELEVES)
    path_csv = exporter_bareme_csv(bareme, FILE_PATH)
