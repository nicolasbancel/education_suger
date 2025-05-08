# filepath: src/utils/chatgpt_prompts.py
from openai import OpenAI

from utils.prompts.latex_prompts import prompt_get_exercices


# from config.settings import OPENAI_API_KEY
import os
import re
from dotenv import load_dotenv
import json
from typing import List, Dict, Tuple, Optional

load_dotenv()


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

EXERCICE_KEYS = {
    "numero_exercice": int,
    "titre_exercice": str,
    "enonce_exercice": str,
    "image_path": str,
    "questions_exercice": list,
}

QUESTION_PATTERN = re.compile(
    r"(\\question(?:\[[^\]]*\])?\s*)(?P<qtext>.*?)(?=(\\question|\\section|\\subsection|\\end\{document\}|\Z))",
    re.DOTALL,
)


LATEX_FILE_PATH = "/Users/nicolasbancel/git/education_suger/02_3ème_CI_pc/ds/brevet_blanc_2_corrige.tex"


def extract_exercises_from_latex(latex_file_path: str) -> List[Dict]:
    """
    Extrait les exercices structurés à partir d’un fichier LaTeX.

    Pour chaque \section{...} ou \section*{...}, on construit un dictionnaire :
        - numero_exercice (int)
        - titre_exercice (str)
        - enonce_exercice (str)
        - image_paths (List[str]) : chemins absolus des images dans l’énoncé
        - questions_exercice : liste de dicts avec :
            - enonce (str)
            - solution (str, vide)
            - marker (str, ex: Q1E2)
            - image_paths (List[str]) : chemins absolus des images dans la question
    """

    with open(latex_file_path, "r", encoding="utf-8") as f:
        raw_latex = f.read()

    base_dir = os.path.dirname(os.path.abspath(latex_file_path))

    section_pattern = re.compile(
        r"\\section\*?{(?P<title>[^}]*)}\s*(?P<content>.*?)(?=(\\section|\\end\{document\}))",
        re.DOTALL,
    )

    image_pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?{(.+?)}")

    exercices = []

    for i, section_match in enumerate(section_pattern.finditer(raw_latex)):
        numero_exercice = i + 1
        title = section_match.group("title").strip()
        content = section_match.group("content").strip()

        question_matches = list(QUESTION_PATTERN.finditer(content))

        if question_matches:
            enonce_exercice = content[: question_matches[0].start()].strip()
        else:
            enonce_exercice = content

        # Toutes les images dans l’énoncé
        image_paths_exo = [
            os.path.abspath(os.path.join(base_dir, m))
            for m in image_pattern.findall(enonce_exercice)
        ]

        questions = []
        for j, q in enumerate(question_matches):
            qtext = q.group("qtext").strip()
            marker = f"Q{j+1}E{numero_exercice}"

            # Toutes les images dans la question
            image_paths_q = [
                os.path.abspath(os.path.join(base_dir, m))
                for m in image_pattern.findall(qtext)
            ]

            questions.append(
                {
                    "enonce": qtext,
                    "solution": "",
                    "marker": marker,
                    "image_paths": image_paths_q,
                }
            )

        exercices.append(
            {
                "numero_exercice": numero_exercice,
                "titre_exercice": title,
                "enonce_exercice": enonce_exercice,
                "image_paths": image_paths_exo,
                "questions_exercice": questions,
            }
        )

    return exercices


def insert_correction_markers_into_latex(latex_path: str, exercices: List[Dict]) -> str:
    """
    Insère dans un fichier LaTeX les marqueurs de correction %CORRECTION:QxEy%
    à la fin de chaque énoncé de question.

    Args:
        latex_path (str): Chemin vers le fichier LaTeX original.
        exercices (List[Dict]): Liste d’exercices structurés contenant les markers.
        output_path (str, optional): Chemin du fichier de sortie. Si None, ajoute '_corrige.tex'.

    Returns:
        str: Chemin du nouveau fichier LaTeX avec marqueurs.
    """
    with open(latex_path, "r", encoding="utf-8") as f:
        raw_latex = f.read()

    updated_latex = raw_latex
    offset = 0  # Décalage causé par les insertions précédentes

    # Regex pour capturer toutes les questions avec leur contenu
    """
    question_pattern = re.compile(
        r"(\\question(?:\[[^\]]*\])?\s*)(.*?)(?=(\\question|\\section|\\subsection|\\end\{document\}))",
        re.DOTALL
    )
    """

    # On crée une liste de tous les (question_text, marker)
    all_markers = []
    for exercice in exercices:
        for question in exercice["questions_exercice"]:
            all_markers.append((question["enonce"], question["marker"]))

    matches = list(QUESTION_PATTERN.finditer(updated_latex))
    for i, match in enumerate(matches):
        if i >= len(all_markers):
            break  # Sécurité

        q_enonce, marker = all_markers[i]

        insertion_point = match.end() + offset
        updated_latex = (
            updated_latex[:insertion_point]
            + f"\n%{marker}%\n"
            + updated_latex[insertion_point:]
        )
        offset += len(f"\n%{marker}%\n")

    if latex_path.endswith(".tex"):
        output_path = latex_path.replace(".tex", "_corrige.tex")
    else:
        output_path = latex_path + "_corrige"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(updated_latex)

    # print(f"✅ Marqueurs insérés dans le fichier : {output_path}")
    return output_path


def extract_exercises_from_latex_8(latex_file_path: str) -> List[Dict]:
    """
    Extrait les exercices structurés à partir d’un fichier LaTeX.

    Pour chaque \section{...} ou \section*{...}, on construit un dictionnaire :
        - numero_exercice (int)
        - titre_exercice (str)
        - enonce_exercice (str)
        - image_path (str | None) si une image est trouvée dans l’énoncé général
        - questions_exercice : liste de dicts avec :
            - enonce
            - solution (vide)
            - marker (de type QxEy)
            - image_path (str | None) si une image est dans la question
    """

    with open(latex_file_path, "r", encoding="utf-8") as f:
        raw_latex = f.read()

    base_dir = os.path.dirname(os.path.abspath(latex_file_path))

    section_pattern = re.compile(
        r"\\section\*?{(?P<title>[^}]*)}\s*(?P<content>.*?)(?=(\\section|\\end\{document\}))",
        re.DOTALL,
    )

    """
    question_pattern = re.compile(
        r"(\\question(?:\[[^\]]*\])?\s*)(?P<qtext>.*?)(?=(\\question|\\subsection|\\section|\\end\{document\}|\\Z))",
        re.DOTALL,
    )
    """

    image_pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?{(.+?)}")

    exercices = []

    for i, section_match in enumerate(section_pattern.finditer(raw_latex)):
        numero_exercice = i + 1
        title = section_match.group("title").strip()
        content = section_match.group("content").strip()

        question_matches = list(QUESTION_PATTERN.finditer(content))

        if question_matches:
            enonce_exercice = content[: question_matches[0].start()].strip()
        else:
            enonce_exercice = content

        image_match_exo = image_pattern.search(enonce_exercice)
        image_path_exo = (
            os.path.abspath(os.path.join(base_dir, image_match_exo.group(1)))
            if image_match_exo
            else None
        )

        questions = []
        for j, q in enumerate(question_matches):
            qtext = q.group("qtext").strip()
            marker = f"Q{j+1}E{numero_exercice}"

            image_match_q = image_pattern.search(qtext)
            image_path_q = (
                os.path.abspath(os.path.join(base_dir, image_match_q.group(1)))
                if image_match_q
                else None
            )

            questions.append(
                {
                    "enonce": qtext,
                    "solution": "",
                    "marker": marker,
                    "image_path": image_path_q,
                }
            )

        exercices.append(
            {
                "numero_exercice": numero_exercice,
                "titre_exercice": title,
                "enonce_exercice": enonce_exercice,
                "image_path": image_path_exo,
                "questions_exercice": questions,
            }
        )

    return exercices


def extract_exercises_from_latex_with_markers(
    latex_path: str, output_path: Optional[str] = None
) -> List[Dict]:
    """
    Parse un fichier LaTeX d'exercices pour en extraire une structure de données,
    insère des marqueurs pour les corrections à la fin de chaque énoncé de question,
    et écrit un nouveau fichier .tex modifié.

    Args:
        latex_path (str): Chemin vers le fichier LaTeX d'entrée.
        output_path (Optional[str]): Chemin vers le fichier de sortie LaTeX avec marqueurs (si None, suffixe '_corrigé' est utilisé).

    Returns:
        List[Dict]: Une liste d'exercices structurés, avec questions, images et marqueurs.
    """
    with open(latex_path, "r", encoding="utf-8") as f:
        raw_latex = f.read()

    base_dir = os.path.dirname(os.path.abspath(latex_path))

    section_pattern = re.compile(
        r"\\section\*?{(?P<title>[^}]*)}\s*(?P<content>.*?)(?=(\\section|\\end\{document\}))",
        re.DOTALL,
    )

    question_pattern = re.compile(
        r"(\\question(?:\[[^\]]*\])?\s*)(?P<qtext>.*?)(?=(\\question|\\subsection|\\section|\\end\{document\}|\Z))",
        re.DOTALL,
    )

    image_pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?{(.+?)}")

    updated_latex = raw_latex  # pour insérer les marqueurs
    offset = 0  # pour ajuster les positions lors des insertions
    exercices = []

    for i, section_match in enumerate(section_pattern.finditer(raw_latex)):
        numero_exercice = i + 1
        title = section_match.group("title").strip()
        content = section_match.group("content")

        section_start = section_match.start("content") + offset

        # Recherche des questions
        questions = []
        for j, q_match in enumerate(question_pattern.finditer(content)):
            numero_question = f"Q{j+1}E{numero_exercice}"
            full_question_start = section_start + q_match.start()
            full_question_text = q_match.group("qtext").strip()

            # Image ?
            image_match = image_pattern.search(full_question_text)
            image_path = (
                os.path.abspath(os.path.join(base_dir, image_match.group(1)))
                if image_match
                else None
            )

            # Marqueur
            marker = f"%CORRECTION:{numero_question}%"

            # Insertion du marqueur juste à la fin de l’énoncé de la question
            full_question_start = section_start + q_match.start("qtext")
            insertion_point = full_question_start + len(q_match.group("qtext").rstrip())

            updated_latex = (
                updated_latex[: insertion_point + offset]
                + "\n\n"
                + marker
                + "\n\n"
                + updated_latex[insertion_point + offset :]
            )
            offset += len(marker) + 2  # maj de l’offset global

            questions.append(
                {
                    "marker": marker,
                    "enonce": full_question_text,
                    "solution": "",
                    "image_path": image_path,
                }
            )

        # Enoncé général de l’exercice
        if questions:
            enonce_exercice = content[
                : question_pattern.search(content).start()
            ].strip()
        else:
            enonce_exercice = content.strip()

        # Image dans l’énoncé ?
        image_match_exo = image_pattern.search(enonce_exercice)
        image_path_exo = (
            os.path.abspath(os.path.join(base_dir, image_match_exo.group(1)))
            if image_match_exo
            else None
        )

        exercices.append(
            {
                "numero_exercice": numero_exercice,
                "titre_exercice": title,
                "enonce_exercice": enonce_exercice,
                "image_path": image_path_exo,
                "questions_exercice": questions,
            }
        )

    # Écriture du fichier corrigé avec marqueurs
    if output_path is None:
        name, ext = os.path.splitext(latex_path)
        output_path = f"{name}_corrige{ext}"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(updated_latex)

    print(f"✅ Fichier LaTeX avec marqueurs sauvegardé : {output_path}")
    return exercices


def extract_exercises_from_latex_no_marker(LATEX_FILE_PATH: str) -> List[Dict]:
    """
    Extrait les exercices structurés à partir d’un fichier LaTeX.

    Pour chaque \section{...} ou \section*{...}, on construit un dictionnaire :
        - numero_exercice (int)
        - titre_exercice (str)
        - enonce_exercice (str)
        - image_path (str | None) si une image est trouvée dans l’énoncé général
        - questions_exercice : liste de dicts avec :
            - numero : QxEy
            - enonce
            - solution (vide)
            - image_path (str | None) si une image est dans la question
    """

    with open(LATEX_FILE_PATH, "r", encoding="utf-8") as f:
        raw_latex = f.read()

    base_dir = os.path.dirname(os.path.abspath(LATEX_FILE_PATH))

    section_pattern = re.compile(
        r"\\section\*?{(?P<title>[^}]*)}\s*(?P<content>.*?)(?=(\\section|\\end\{document\}))",
        re.DOTALL,
    )

    question_pattern = re.compile(
        r"(\\question(?:\[[^\]]*\])?\s*)(?P<qtext>.*?)(?=(\\question|\\subsection|\\section|\\end\{document\}|\Z))",
        re.DOTALL,
    )

    image_pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?{(.+?)}")

    exercices = []

    for i, section_match in enumerate(section_pattern.finditer(raw_latex)):
        numero_exercice = i + 1
        title = section_match.group("title").strip()
        content = section_match.group("content").strip()

        question_matches = list(question_pattern.finditer(content))

        if question_matches:
            enonce_exercice = content[: question_matches[0].start()].strip()
        else:
            enonce_exercice = content

        # Image dans l'énoncé général ?
        image_match_exo = image_pattern.search(enonce_exercice)
        image_path_exo = (
            os.path.abspath(os.path.join(base_dir, image_match_exo.group(1)))
            if image_match_exo
            else None
        )

        questions = []
        for j, q in enumerate(question_matches):
            qtext = q.group("qtext").strip()
            numero = f"Q{j+1}E{numero_exercice}"

            image_match_q = image_pattern.search(qtext)
            image_path_q = (
                os.path.abspath(os.path.join(base_dir, image_match_q.group(1)))
                if image_match_q
                else None
            )

            questions.append(
                {
                    "numero": numero,
                    "enonce": qtext,
                    "solution": "",
                    "image_path": image_path_q,
                }
            )

        exercices.append(
            {
                "numero_exercice": numero_exercice,
                "titre_exercice": title,
                "enonce_exercice": enonce_exercice,
                "image_path": image_path_exo,
                "questions_exercice": questions,
            }
        )

    return exercices


def add_image_paths_to_exercices(
    exercices: List[Dict], latex_file_path: str
) -> List[Dict]:
    """
    Parcourt les exercices et leurs questions pour ajouter une clé 'image_path'
    si une image LaTeX (\includegraphics) est détectée dans l'énoncé.
    Le chemin est résolu en absolu depuis le dossier contenant le fichier .tex.

    Args:
        exercices (List[Dict]): liste des exercices structurés
        latex_file_path (str): chemin absolu vers le fichier LaTeX source

    Returns:
        List[Dict]: même liste, enrichie avec les clés 'image_path' si pertinent
    """
    base_dir = os.path.dirname(os.path.abspath(latex_file_path))
    img_pattern = re.compile(r"\\includegraphics(?:\[.*?\])?{(.+?)}")

    for ex in exercices:
        # Cherche une image dans l'énoncé général
        match = img_pattern.search(ex["enonce_exercice"])
        if match:
            rel_path = match.group(1)
            ex["image_path"] = os.path.abspath(os.path.join(base_dir, rel_path))

        # Cherche dans chaque question
        for q in ex["questions_exercice"]:
            match = img_pattern.search(q["enonce"])
            if match:
                rel_path = match.group(1)
                q["image_path"] = os.path.abspath(os.path.join(base_dir, rel_path))

    return exercices


## METHODE AVEC OPENAI ##


def get_exercice_openai(latex_file_path):
    prompt = prompt_get_exercices(latex_file_path)
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Tu es un assistant pédagogique.\n"
                "On te fournit un document LaTeX contenant plusieurs exercices.\n"
                "Ta tâche est d'extraire une liste d'objets JSON avec **exactement** les champs suivants :\n"
                "- `numero_exercice` (int) : numéro d'ordre de l'exercice\n"
                "- `titre_exercice` (str) : le titre brut de l'exercice (extrait de \\section{})\n"
                "- `enonce_exercice` (str) : le texte d'introduction avant les questions\n"
                "- `questions_exercice` (list[str]) : chaque élément est le contenu d'une balise \\question{}\n\n"
                "Ta réponse doit être **un tableau JSON valide**, sans aucun texte ou code Python autour.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                ],
            },
        ],
    )
    print("Response: ", response)
    raw_string = response.output[0].content[0].text
    try:
        output = json.loads(raw_string)
    except json.JSONDecodeError as e:
        print("Erreur de décodage JSON : ", e)

    return output


def insert_solution_placeholder(exercices: list[dict]) -> list[dict]:
    """
    Pour chaque exercice dans la liste, transforme la liste 'questions_exercice'
    en une liste de dictionnaires {'enonce': ..., 'solution': ''}.
    """
    """
    Transforme chaque chaîne de la liste 'questions_exercice' en dict {'enonce': ..., 'solution': ''}.
    Modifie la structure en place et retourne la nouvelle liste.
    """
    for exercice in exercices:
        exercice["questions_exercice"] = [
            {"enonce": question, "solution": ""}
            for question in exercice["questions_exercice"]
        ]
    print("✅ Done : Insertion des placeholders de solutions.")
    return exercices


if __name__ == "__main__":

    open_ai_method = False
    LATEX_FILE_PATH = (
        "/Users/nicolasbancel/git/education_suger/02_3ème_CI_pc/ds/brevet_blanc_2.tex"
    )
    LATEX_FILE_PATH_MARKERS = "/Users/nicolasbancel/git/education_suger/02_3ème_CI_pc/ds/brevet_blanc_2_testmarkers.tex"

    if open_ai_method:
        exercices = get_exercices(LATEX_FILE_PATH)
        print("Exercices : ", exercices)
        exercices = insert_solution_placeholder(exercices)
    else:
        exercices = extract_exercises_from_latex(LATEX_FILE_PATH)
        print("Exercices : ", exercices)
        output_path = insert_correction_markers_into_latex(
            LATEX_FILE_PATH, exercices, LATEX_FILE_PATH_MARKERS
        )
        print("Output_path : ", output_path)
