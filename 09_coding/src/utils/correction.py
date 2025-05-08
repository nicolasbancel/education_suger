# filepath: src/utils/chatgpt_prompts.py
from openai import OpenAI

# from config.settings import OPENAI_API_KEY
import sys
import base64
import os
import json
from typing import List
from PIL import Image
from dotenv import load_dotenv


load_dotenv()


IMAGE_PATH_GLOBAL = (
    "/Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg"
)

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

CLASSE = "1ère STD2A"
DATE = "5 Mai 2025"
MATIERE = "Physique-Chimie"
IMAGE_PATH = "/Users/nicolasbancel/git/education_suger/09_coding/data/exo_18.jpg"
PACKAGES_PATH = "/Users/nicolasbancel/git/education_suger/mypackages.sty"
CONTRAINTES_PATH = "/Users/nicolasbancel/git/education_suger/09_coding/templates/contraintes_physique.md"
LATEX_TEMPLATE = "/Users/nicolasbancel/git/education_suger/09_coding/templates/template_correction.tex"
OUTPUT_DIR = "correction"
IMAGE_FOLDER = "/Users/nicolasbancel/git/education_suger/09_coding/data/a_corriger"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


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


def make_image_block(image_path: str) -> str:
    """
    Génère un bloc LaTeX pour insérer une image avec une légende.
    """
    return rf"""\begin{{figure}}[H]
  \centering
  \includegraphics[width=0.6\linewidth]{{{image_path}}}
  \captionsetup{{labelformat=empty}}
\end{{figure}}"""


def update_latex(
    latex_template_path: str,
    output_dir: str,
    classe: str,
    date: str,
    matiere: str,
):
    """
    Remplit le template LaTeX avec les valeurs fournies et écrit un nouveau fichier compilable.
    """

    with open(latex_template_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Remplacements simples via des balises uniques
    replacements = {
        "[[CLASSE]]": classe,
        "[[DATE]]": date,
        "[[MATIERE]]": matiere,
    }

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    # Génère un nom de fichier en fonction de la classe et de la date
    filename = f"fiche_{classe.replace(' ', '')}_{date.replace(' ', '-')}.tex"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

    full_path = os.path.abspath(output_path)
    print(f"✅ Fichier LaTex généré : {full_path}")
    return full_path


def correction(
    image_path,
    contraintes_path,
    packages_path=PACKAGES_PATH,
):
    """
    Renvoie les coordonnées du pixel en haut à gauche de l'encadré qui correspond à l'exercice et au suivant
    Tout est fait en un seul prompt
    """

    # Encodage de l'image
    base64_image = encode_image(image_path)

    with open(contraintes_path, encoding="utf-8") as f:
        contraintes = f.read()

    if packages_path:
        with open(packages_path, encoding="utf-8") as p:
            packages_text = p.read()

    system_prompt = (
        "Tu es un assistant qui génère des corrections d'exercices en LaTeX.\n\n"
        "Voici les consignes à suivre impérativement pour rédiger la correction :\n\n"
        f"{contraintes}\n\n"
        "Tu dois utiliser les packages suivants :\n"
        f"{packages_text}\n\n"
        "Ta réponse doit commencer par \\begin{{solution}} et se terminer par \\end{{solution}}, sans rien autour."
    )

    prompt_box = (
        "Tu es un modèle de vision artificielle. On te fournit une image scannée d'un exercice"
        "Tu dois rédiger une solution en format LaTex qui commence par \begin{solution} et se termine par \end{solution}"
    )
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt_box},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ],
    )

    # print("Response: ", response)
    try:
        raw_content = response.output[0].content[0].text.strip()

        # Cas 1 : réponse formatée avec bloc Markdown ```latex ... ```
        if raw_content.startswith("```latex"):
            latex_correction = raw_content.strip("```latex").strip("`").strip()
        else:
            latex_correction = raw_content.strip()

        return latex_correction

    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction du contenu LaTeX : {e}")


def latex_block(
    latex_correction,
    latex_file_path,
    image_path,
):
    system_prompt = "Tu es un assistant qui trouve des titres à des exercices"

    prompt = (
        "On te fournit une correction d'exercice en Latex. A partir de cette correction, trouve un titre à l'exercice"
        "En sortie, ne me donne que le titre, sans rien autour. Fais un titre succinct et explicite."
        "Voici la correction :\n"
        f"{latex_correction}"
    )

    title_raw = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                ],
            },
        ],
    )

    # print("Response: ", title_raw)
    try:
        title = title_raw.output[0].content[0].text.strip()
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction du contenu LaTeX : {e}")

    latex_block = rf"""
    \section*{{{title}}}

    \begin{{figure}}[H]
      \centering
      \includegraphics[width=0.6\linewidth]{{{image_path}}}
      \captionsetup{{labelformat=empty}}
    \end{{figure}}

    {latex_correction}
    """.strip()

    try:
        with open(latex_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if r"\end{document}" not in content:
            raise ValueError(
                r"La balise \end{document} est introuvable dans le fichier."
            )

        updated_content = content.replace(
            r"\end{document}", f"\n\n{latex_block}\n\n\\end{{document}}"
        )

        with open(latex_file_path, "w", encoding="utf-8") as file:
            file.write(updated_content)

        print(f"✅ Correction faite et insérée pour : {os.path.basename(image_path)}")

    except Exception as e:
        print(f"❌ Erreur lors de l'injection LaTeX : {e}")


if __name__ == "__main__":
    # Exemple d'utilisation

    images = get_image_files(IMAGE_FOLDER)

    latex_file_path = update_latex(
        latex_template_path=LATEX_TEMPLATE,
        output_dir=OUTPUT_DIR,
        classe=CLASSE,
        date=DATE,
        matiere=MATIERE,
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
