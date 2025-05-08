from openai import OpenAI
from utils.latex_parser import get_exercice_openai, insert_solution_placeholder
from utils.helpers import encode_image
from dotenv import load_dotenv
import os
import re
import shutil
from pathlib import Path

load_dotenv()

LATEX_FILE_PATH = (
    "/Users/nicolasbancel/git/education_suger/02_3ème_CI_pc/ds/brevet_blanc_2.tex"
)
CONTRAINTES_PATH = "/Users/nicolasbancel/git/education_suger/09_coding/templates/contraintes_physique.md"
PACKAGES_PATH = "/Users/nicolasbancel/git/education_suger/mypackages.sty"
LATEX_PROMPT_CORRECTION = "/Users/nicolasbancel/git/education_suger/09_coding/src/utils/prompts/from_latex/latex_prompt_correction.md"

#### A CORRIGER ####
RAW_LATEX_FILE_PATH = (
    "/Users/nicolasbancel/git/education_suger/02_3ème_CI_pc/ds/brevet_blanc_2.tex"
)

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def solution_question(exercices, question_context, info):
    """
    Génère une solution LaTeX pour une question en utilisant l'API OpenAI.

    Arguments :
        - exercices : structure complète (avec les autres exercices/réponses)
        - question_context : contexte d’un exercice (titre, énoncé, réponses en cours)
        - marker : identifiant de type QxEy
        - enonce_question : texte de la question
        - image_paths : liste des chemins des images associées à la question
        - LATEX_PROMPT_CORRECTION : chemin vers le fichier prompt
        - CONTRAINTES_PATH : chemin vers les contraintes LaTeX
        - PACKAGES_PATH : chemin vers les packages
        - client : instance OpenAI

    Retour :
        - La correction en LaTeX (string)
    """

    replacements = {
        "[[QUESTION]]": info["enonce_question"],
        # "[[ENONCE_ENTIER]]": raw_latex, # pas sur que ce soit réellement utile
        "[[ENONCE_STRUCTURE_AVEC_REPONSE]]": question_context,
    }

    # Make the prompt more robust
    # by replacing the placeholders with the actual values
    with open(LATEX_PROMPT_CORRECTION, "r", encoding="utf-8") as file:
        prompt = file.read()

    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, str(value))

    with open(CONTRAINTES_PATH, encoding="utf-8") as f:
        contraintes = f.read()

    with open(PACKAGES_PATH, encoding="utf-8") as p:
        packages_text = p.read()

    system_prompt = (
        "Tu es un assistant qui génère des corrections d'exercices en LaTeX.\n\n"
        "Voici les consignes à suivre impérativement pour rédiger la correction :\n\n"
        f"{contraintes}\n\n"
        "Tu dois utiliser les packages suivants :\n"
        f"{packages_text}\n\n"
        "Ta réponse doit commencer par \begin{solution} et se terminer par \end{solution}, sans rien autour."
        "Il ne doit pas y avoir de balise \begin{question} ou \end{question} dans la réponse."
    )

    user_content = [{"type": "input_text", "text": prompt}]
    if len(info["image_paths"]) > 0:
        for image_path in info["image_paths"]:
            try:
                image_b64 = encode_image(image_path)
                user_content.append(
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_b64}",
                    }
                )
            except Exception as e:
                print(f"Erreur lors de l'encodage de {image_path} : {e}")

            # Appel API
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )

    try:
        correction = response.output[0].content[0].text.strip()
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction du contenu LaTeX : {e}")

    correction = correction.strip().removeprefix("```latex").removesuffix("```").strip()
    correction = re.sub(r"\\begin{questions}", "", correction)
    correction = re.sub(r"\\end{questions}", "", correction)

    # Update de la variable exercices qui contient tout le DS structuré avec les réponses
    print(f"✅ Correction trouvée pour question : {info['marker']}")
    exercices[info["index_exercice"]]["questions_exercice"][info["index_question"]][
        "solution"
    ] = correction

    # Pas besoin de return - à priori la réponse a déjà été updatée
    # return exercices


def copy_latex_file_for_correction(source_path: str) -> str:
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    destination = source.with_name(source.stem + "_corrige.tex")
    shutil.copyfile(source, destination)

    print(f"✅ Copied to: {destination}")
    return str(destination)


def insert_solutions_into_latex(output_path: str, exercices: list):
    """
    Remplace les marqueurs de correction %CORRECTION:QxEy% dans un fichier LaTeX par les solutions correspondantes.

    Args:
        output_path (str): Chemin du fichier LaTeX à modifier (il contient déjà les marqueurs).
        exercices (list): Liste d'exercices structurés contenant les solutions associées à chaque question.

    Cette fonction écrase le fichier LaTeX original avec les solutions insérées.
    """

    # Lire le fichier existant contenant les marqueurs
    with open(output_path, "r", encoding="utf-8") as f:
        latex_text = f.read()

    # Remplacement des marqueurs par les solutions
    for exercice in exercices:
        for question in exercice["questions_exercice"]:
            marker = f"%{question['marker']}%"
            solution = question["solution"].strip()
            replacement = f"\n{solution}\n"
            if marker in latex_text:
                latex_text = latex_text.replace(marker, replacement)
                print(f"✅ Marqueur remplacé : {marker}")
            else:
                print(f"⚠️ Marqueur introuvable : {marker}")

    # Sauvegarde du fichier corrigé (même nom : écrasement)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(latex_text)

    print(f"✅ Les solutions ont été insérées dans : {output_path}")


if __name__ == "__main__":

    structured_latex = get_exercice_openai(LATEX_FILE_PATH)
    structured_questions = insert_solution_placeholder(structured_latex)
    structured_questions_backup = structured_questions.copy()

    with open(RAW_LATEX_FILE_PATH, "r", encoding="utf-8") as file:
        raw_latex = file.read()

    for index_exercice, exercice in enumerate(structured_questions):
        print(
            f"Traitement de Exercice {index_exercice + 1} : {exercice['titre_exercice']}"
        )
        for index_question, question in enumerate(exercice["questions_exercice"]):
            solution = solution_question(
                raw_latex,
                structured_questions,
                exercice["questions_exercice"][index_question]["enonce"],
            )
            # Update de structured_questions pour fournir encore plus de contexte à la question suivante
            structured_questions[index_exercice]["questions_exercice"][index_question][
                "solution"
            ] = solution
            print(f"✅ Question {index_question + 1} résolue")

    print("✅ Toutes les questions ont été résolues.")

    # Test sur le 1er element
    # question = structured_questions[0]["questions_exercice"][0]["enonce"]
    # solution = solution_question(raw_latex, structured_questions, question)
