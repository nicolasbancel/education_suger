# Contents of /auto-correct-tool/auto-correct-tool/src/main.py

import os
import sys
import argparse
import shutil
from pathlib import Path


sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    from dotenv import load_dotenv

    # Cherche le .env à la racine du repo (un cran au-dessus de /src)
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    ENV_PATH = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=ENV_PATH, override=False)
except Exception as e:
    print(f"⚠️ Impossible de charger .env automatiquement ({e}).")

# 1) --- Corriger le sys.path pour viser .../<repo>/src, pas .../src/src ---
REPO_ROOT = (
    Path(__file__).resolve().parents[1]
)  # .../auto-correct-tool/auto-correct-tool
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from utils.helpers import (
    extract_class_and_subject_from_path,
    get_date_format_francais,
    get_image_files,
    save_variable_to_json,
)
from utils.latex_parser import (
    extract_exercises_from_latex,
    insert_correction_markers_into_latex,
    get_exercice_openai,
    insert_solution_placeholder,
)

from config import CONTRAINTES_PATH, PACKAGES_PATH, LATEX_TEMPLATE
from utils.correction.from_latex import solution_question, insert_solutions_into_latex
from utils.correction.from_image import correction, latex_block, update_latex


def run_from_image(folder_path):
    if not os.path.isdir(folder_path):
        print(f"❌ Le dossier spécifié n'existe pas : {folder_path}")
        sys.exit(1)
    print(f"📸 Traitement des images dans le dossier : {folder_path}")

    classe, matiere = extract_class_and_subject_from_path(folder_path)
    images = get_image_files(folder_path)

    # Déterminer le dossier d'output
    input_path = Path(folder_path)
    output_dir = input_path.parent

    latex_file_path = update_latex(
        latex_template_path=LATEX_TEMPLATE,
        output_dir=output_dir,
        classe=classe,
        date=get_date_format_francais(),
        matiere=matiere,
    )

    for image in images:

        latex_correction = correction(
            image_path=image,
            contraintes_path=CONTRAINTES_PATH,
            packages_path=PACKAGES_PATH,
        )

        latex_block(
            latex_correction,
            latex_file_path,
            image_path=image,
        )


def run_from_latex(
    file_path, open_ai_method=False, export_exercices=True, export_markers=True
):
    if not os.path.isfile(file_path) or not file_path.endswith(".tex"):
        print(f"❌ Fichier LaTeX invalide : {file_path}")
        sys.exit(1)
    print(f"📄 Traitement du fichier LaTeX : {file_path}")
    if open_ai_method:
        exercices = get_exercice_openai(file_path)
        print("Exercices : ", exercices)
        exercices = insert_solution_placeholder(exercices)
    else:
        exercices = extract_exercises_from_latex(file_path)
        print("Exercices : ", exercices)
        output_path = insert_correction_markers_into_latex(file_path, exercices)
        print("✅ Markers inserted in Output_path : ", output_path)

        if export_markers:
            original = Path(output_path)
            if "_corrige.tex" in original.name:
                new_name = original.name.replace("_corrige.tex", "_markers.tex")
            else:
                new_name = original.stem + "_markers.tex"

            new_path = original.with_name(new_name)
            shutil.copyfile(original, new_path)
            print(
                f"✅ Copie du fichier avec les marqueurs enregistrée sous : {new_path}"
            )

        question_context = {}
        for index_exercice, exercice in enumerate(exercices):
            images_list = exercice.get("image_paths", [])
            # on génère ici une version plus succincte du contexte de la question
            # qui comprendra la question, les réponses aux questions précédentes  de l'exercice, et l'énoncé global et images de l'exercice

            keys_to_extract = [
                "numero_exercice",
                "titre_exercice",
                "enonce_exercice",
                "image_paths",
            ]
            question_context = {
                key: exercice[key] for key in keys_to_extract if key in exercice
            }
            for index_question, question in enumerate(exercice["questions_exercice"]):
                marker = question["marker"]
                enonce = question["enonce"]
                question_context["questions_exercice"] = exercice["questions_exercice"][
                    0 : index_question + 1
                ]
                print(
                    f"✅ Context for Exercice {index_exercice + 1} - Question {index_question + 1} : Context : {question_context}"
                )

                info = {
                    "index_exercice": index_exercice,
                    "index_question": index_question,
                    "marker": marker,
                    "image_paths": images_list,
                    "enonce_question": enonce,
                }

                solution_question(exercices, question_context, info)

                print("✅ New version of the exercices variable : ", exercices)

        insert_solutions_into_latex(output_path, exercices)
        if export_exercices:
            save_variable_to_json(exercices, file_path)


def run_from_pdf(file_path):
    if not os.path.isfile(file_path) or not file_path.endswith(".pdf"):
        print(f"❌ Fichier PDF invalide : {file_path}")
        sys.exit(1)
    print(f"📚 Traitement du fichier PDF : {file_path}")
    # TODO: appeler ta fonction from_pdf ici


def main():
    parser = argparse.ArgumentParser(description="Correction automatique d'exercices.")
    parser.add_argument(
        "mode",
        choices=["from_image", "from_latex", "from_pdf"],
        help="Mode de correction à utiliser",
    )
    parser.add_argument(
        "input_path", help="Chemin vers le dossier ou fichier à traiter"
    )

    args = parser.parse_args()

    if args.mode == "from_image":
        run_from_image(args.input_path)
    elif args.mode == "from_latex":
        run_from_latex(args.input_path)
    elif args.mode == "from_pdf":
        run_from_pdf(args.input_path)
    else:
        print("❌ Mode non reconnu.")
        sys.exit(1)


if __name__ == "__main__":
    main()
    # en command lines
    # poetry run python main.py --d /Users/nicolasbancel/git/education_suger/01_1ères_STD2A_pc/chap5_lumiere/a_corriger
    # poetry run python main.py --mode from_latex --input_path /Users/nicolasbancel/git/education_suger/02_3ème_CI_pc/ds/brevet_blanc_2.tex
