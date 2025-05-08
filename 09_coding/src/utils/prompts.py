# filepath: src/utils/chatgpt_prompts.py
from openai import OpenAI

# from config.settings import OPENAI_API_KEY
import sys
import base64
import os
import json
from pydantic import BaseModel
from typing import List
from PIL import Image
from dotenv import load_dotenv

from utils.helpers import encode_image


load_dotenv()


NUMEROTATION_EXERCICES = {
    "Physique_1ères": "Chaque exercice est identifié par un numéro placé dans un carré bleu, en gras, "
    "généralement situé en haut à gauche du bloc d'énoncé. "
    "Ce carré est petit, visuellement distinct par sa couleur bleue et ne contient que le numéro (ex: 18, 19...). ",
    "Maths_1ères": "Chaque exercice est identifié par un numéro placé dans un carré bleu, en gras, en haut à gauche du bloc de l'énoncé",
}

IMAGE_PATH = (
    "/Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg"
)


class Exercice_Coordinates(BaseModel):
    top_left: List[str]
    bottom_right: List[str]


# openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

print(os.environ.get("OPENAI_API_KEY"))

# Documentation on how to extract the image
# https://platform.openai.com/docs/guides/images-vision?api-mode=responses&format=base64-encoded


def column_size(image_path):
    """
    Returns the size of the columns
    """
    # with open(image_path, "rb") as image_file:
    #    image_data = image_file.read()
    # files = {"file": ("image.jpg", image_data, "image/jpg")}
    with Image.open(image_path) as image:
        print("Image size:", image.size)
        width, height = image.size

    base64_image = encode_image(image_path)

    prompt_columns = (
        "Tu es un modèle de vision artificielle. On te fournit une image scannée d'une feuille d'exercices. "
        "Chaque exercice est numéroté et se suit de la gauche vers la droite, du haut vers le bas. "
        "Les exercices sont répartis en plusieurs colonnes, séparées par des marges verticales (espaces blancs). "
        "On te demande de déterminer la largeur de chaque colonne (c'est-à-dire l'espace horizontal occupé par chaque colonne contenant des exercices), en pixels. "
        "Si la page est divisée en 4 colonnes, tu devras donner une liste de 4 entiers correspondant aux largeurs de ces colonnes. "
        "Tu dois t'assurer que la somme de ces largeurs soit égale à la largeur totale de l'image. "
        f"Les dimensions de l'image sont : Largeur = {width} pixels, Hauteur = {height} pixels. "
        "Ta réponse doit être uniquement une liste d'entiers représentant les largeurs de chaque colonne, sans explication ni commentaire."
    )
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Tu es un assistant vision IA très précis. Tes réponses sont uniquement sous forme de liste, sans commentaire",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt_columns},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ],
    )
    print("Response: ", response)
    output_text = response.output[0].content[0].text
    print("Output_text: ", output_text)

    try:
        output_list = eval(output_text.strip())
        if (
            isinstance(output_list, list)
            and all(isinstance(x, int) for x in output_list)
            and sum(output_list) == width
        ):
            print("Output_list: ", output_list)
            return output_list
        else:
            raise ValueError(
                "La liste n'est pas valide ou ne correspond pas à la largeur totale de l'image."
            )
    except Exception as e:
        raise ValueError(f"Erreur lors du parsing ou validation : {e}")


def get_num_exercices(image_path):
    """
    Renvoie le nombre d'exercices sur l'image
    """
    prompt_nombre_exos = "Combien d'exercices sont présents sur cette image ? Fais bien la différence entre un exercice et une question. Un exercice est composé d'un énoncé, de questions, et parfois d'images et de graphiques."

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    files = {"file": ("image.jpg", image_data, "image/jpg")}
    base64_image = encode_image(image_path)

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Tu es un modèle de vision artificielle. On te fournit une image scannée d'une feuille d'exercices. Ta réponse est uniquement un nombre, sans commentaire",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt_nombre_exos},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ],
    )
    print("Response: ", response)
    output_text = response.output[0].content[0].text
    print("Output_text: ", output_text)

    try:
        number = int(output_text.strip())
        return number
    except Exception as e:
        raise ValueError(f"Erreur lors de la conversion en nombre : {e}")


def exercice_number_pixel_2(
    image_path,
    exercise_number,
    box_description=NUMEROTATION_EXERCICES["Physique_1ères"],
):
    """
    Renvoie les bounding box de l'encadré de l'exercice
    """

    with Image.open(image_path) as image:
        width, height = image.size

    base64_image = encode_image(image_path)

    prompt = (
        "Tu es un modèle de vision artificielle. On te fournit une image scannée d'une feuille d'exercices. "
        "Chaque exercice est numéroté et se suit de la gauche vers la droite, du haut vers le bas. "
        f"{box_description} "
        f"Tu dois identifier les boîtes englobantes simplement le numéro des exercices {exercise_number} et {exercise_number + 1}. "
        "Cela n'inclut que le numéro de l'exercice. Pas le texte ou l'énoncé."
        "Donne une seule réponse au format JSON de la forme suivante :\n"
        "[\n"
        f'  {{"exercice": {exercise_number}, "bounding_box": {{"top_left": [x1, y1], "bottom_right": [x2, y2]}}}},\n'
        f'  {{"exercice": {exercise_number + 1}, "bounding_box": {{"top_left": [x3, y3], "bottom_right": [x4, y4]}}}}\n'
        "]\n"
        f"Les dimensions de l'image sont : largeur = {width}px, hauteur = {height}px. "
        "N'inclus aucune explication ou commentaire."
    )

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Tu es un assistant vision IA très précis. Tes réponses sont uniquement sous forme de liste, sans commentaire",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ],
    )

    output_raw = response.output[0].content[0].text
    print(f"Output_raw: ", output_raw)
    # output_list.append(output_raw.strip())

    # Parsing propre du JSON renvoyé
    try:
        output_clean = json.loads(output_raw.strip())
        assert isinstance(output_clean, list)
        for entry in output_clean:
            assert "exercice" in entry
            assert "bounding_box" in entry
            assert "top_left" in entry["bounding_box"]
            assert "bottom_right" in entry["bounding_box"]
        return output_clean

    except Exception as e:
        raise ValueError(f"Erreur lors du parsing de la réponse GPT : {e}")


def exercice_number_pixel_archived(
    image_path,
    exercise_number,
    box_description=NUMEROTATION_EXERCICES["Physique_1ères"],
):
    """
    Renvoie les coordonnées du pixel en haut à gauche de l'encadré qui correspond à l'exercice et au suivant
    Tout est fait en deux prompts
    """

    with Image.open(image_path) as image:
        print("Image size:", image.size)
        width, height = image.size

    base64_image = encode_image(image_path)

    output_list = []
    for i in range(2):
        prompt = (
            "Tu es un modèle de vision artificielle. On te fournit une image scannée d'une feuille d'exercices. "
            "Chaque exercice est numéroté et se suit de la gauche vers la droite, du haut vers le bas. "
            f"{box_description} "
            f"Tu dois déterminer le pixel en haut à gauche de l'encadré qui correspond à l'exercice {exercise_number + i} \n"
            f"Les dimensions de l'image sont : Largeur = {width} pixels, Hauteur = {height} pixels. Les coordonées du pixel doivent donc se situer entre ces 2 valeurs"
            f"Ta réponse doit être une liste Python contenant deux entiers [x1, y1], sans explication ni commentaire"
        )
        response = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "system",
                    "content": "Tu es un assistant vision IA très précis. Tes réponses sont uniquement sous forme de liste, sans commentaire",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                },
            ],
        )
        output_raw = response.output[0].content[0].text
        print(f"Output_raw for exercice: {exercise_number + i}", output_raw)
        output_list.append(output_raw.strip())

    return output_list


def exercice_number_pixel_1(
    image_path,
    exercise_number,
    box_description=NUMEROTATION_EXERCICES["Physique_1ères"],
):
    """
    Renvoie les coordonnées du pixel en haut à gauche de l'encadré qui correspond à l'exercice et au suivant
    Tout est fait en un seul prompt
    """

    with Image.open(image_path) as image:
        print("Image size:", image.size)
        width, height = image.size

    base64_image = encode_image(image_path)

    prompt_box = (
        "Tu es un modèle de vision artificielle. On te fournit une image scannée d'une feuille d'exercices. "
        "Chaque exercice est numéroté et se suit de la gauche vers la droite, du haut vers le bas. "
        f"{box_description}"
        "On te demande de déterminer 2 choses :"
        f"(1) le pixel en haut à gauche de l'encadré qui correspond à l'exercice {exercise_number} \n"
        f"(2) le pixel en haut à gauche de l'encadré qui correspond à l'exercice {exercise_number + 1} \n"
        f"Les dimensions de l'image sont : Largeur = {width} pixels, Hauteur = {height} pixels. "
        f"Ta réponse doit être une liste Python contenant deux sous-listes, chacune contenant deux entiers : "
        f"[[x1, y1], [x2, y2]], sans explication ni commentaire"
    )
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Tu es un assistant vision IA très précis. Tes réponses sont uniquement sous forme de liste, sans commentaire",
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
    print("Response: ", response)
    output_raw = response.output[0].content[0].text
    print("Output_rax: ", output_raw)

    try:
        output_list = eval(output_raw.strip())
        if (
            isinstance(output_list, list)
            and len(output_list) == 2
            and all(
                isinstance(coord, list) and len(coord) == 2 for coord in output_list
            )
        ):
            return output_list
        else:
            raise ValueError("Le format de sortie n'est pas valide.")
    except Exception as e:
        raise ValueError(f"Erreur lors du parsing de la sortie : {e}")
    return output_list


if __name__ == "__main__":

    # dotenv -f .env run poetry run python utils/chatgpt_prompts.py /Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg 20

    # /Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg
    # 20

    # poetry run python chatgpt_prompts.py /Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg 20

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    print(os.environ.get("OPENAI_API_KEY"))

    if len(sys.argv) < 3:
        print("Usage: python chatgpt_prompts.py <image_path> <exercise_number>")
        sys.exit(1)

    image_path = sys.argv[1]
    print("Image Path:", image_path)
    exercise_number = sys.argv[2]
    print("Exercise Number:", exercise_number)

    try:
        crop_coordinates = get_crop_coordinates(image_path, exercise_number)
        print("Crop Coordinates:", crop_coordinates)
        crop_coordinates_json = clean_coordinates(crop_coordinates)
        print("Crop Coordinates JSON:", crop_coordinates_json)

    except Exception as e:
        print("Error getting crop coordinates:", e)
