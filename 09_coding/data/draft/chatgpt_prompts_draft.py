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


load_dotenv()


NUMEROTATION_EXERCICES = {
    "Physique_1ères": "Chaque exercice est identifié par un numéro placé dans un carré bleu, en gras, en haut à gauche du bloc d'exercice.",
    "Maths_1ères": "Chaque exercice est identifié par un numéro placé dans un carré bleu, en gras, en haut à gauche du bloc d'exercice.",
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


def get_crop_coordinates(image_path, exercise_number):
    """
    Sends a description of the image to ChatGPT to identify crop coordinates.
    """
    # with open(image_path, "rb") as image_file:
    #    image_data = image_file.read()
    # files = {"file": ("image.jpg", image_data, "image/jpg")}
    with Image.open(image_path) as image:
        print("Image size:", image.size)
        width, height = image.size

    base64_image = encode_image(image_path)

    prompt_1 = (
        f"Étant donné le fichier image suivant et le numéro de l'exercice {exercise_number}, "
        f"identifie les coordonnées en pixels des coins à découper qui délimitent l'exercice sur la page."
        f"Le centre du repère est le coin supérieur gauche de l'image, et tu veilleras à respecter que les coordonnées n'excèdent pas "
        f"les dimensions de l'image (Largeur : {width} x Hauteur : {height}). "
        f"Le format attendu est un dictionnaire JSON avec les clés 'top_left' et 'bottom_right',"
        f"{{'top_left': [x1, y1], 'bottom_right': [x2, y2]}}."
    )

    prompt_2 = (
        f"Tu es un modèle de vision artificielle. On te fournit une image scannée d'une feuille d'exercice, "
        "Chaque exercice est numéroté et se suit de la gauche vers la droite, du haut vers le bas."
        f"et on te demande de localiser précisément tout le texte et les schémas de l'exercice numéro {exercise_number} sur la page. "
        "Donne les coordonnées en pixels des coins opposés de la boîte qui encadre entièrement cet exercice. "
        "Le centre du repère est le coin supérieur gauche de l'image, et tu veilleras à respecter que les coordonnées n'excèdent pas "
        f"les dimensions de l'image (Largeur : {width} x Hauteur : {height}). "
        "Réponds uniquement avec un objet JSON de la forme :\n"
        "{'top_left': [x1, y1], 'bottom_right': [x2, y2]}\n"
        "Les coordonnées doivent être des entiers positifs. Ne propose aucune explication ou conseil, uniquement l'objet JSON."
    )

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Tu es un assistant vision IA très précis. Tes réponses sont uniquement en JSON.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt_2},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ],
        # response_format=Exercice_Coordinates,
        # response_format="json",
        # {"type": "json_object"}
    )
    print("Response: ", response)
    try:
        output_text = response.output[0].content[0].text
        print("Output_text: ", output_text)
    except:
        output_text = None
        raise ValueError(
            "Invalid response format. Expected JSON with 'top_left' and 'bottom_right' keys."
        )
    return output_text


# response['choices'][0]['message']['content']


def clean_coordinates(text):
    key_0 = Exercice_Coordinates.model_json_schema()["required"][0]
    key_1 = Exercice_Coordinates.model_json_schema()["required"][1]
    key_0_type = Exercice_Coordinates.model_json_schema()["properties"][key_0]["type"]
    key_1_type = Exercice_Coordinates.model_json_schema()["properties"][key_1]["type"]
    prompt = (
        f"Tu es un modèle spécialisé dans le fait de générer des dictionnaires JSON à partir d'un format texte."
        f"Transforme le texte suivant : {text} en un dictionnaire JSON qui possède les clés suivantes:"
        f"{key_0} et {key_1} "
        f"qui sont des clés de type {key_0_type} et {key_1_type} respectivement."
        "Tu n'incluras aucune autre information dans ta réponse, pas de ```json, ni de quelconque autre tique"
    )
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Tu es une IA qui convertit des données en JSON. Tes réponses sont uniquement en JSON.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                ],
            },
        ],
    )
    output_text = response.output[0].content[0].text
    print("Output text (fonction clean coordinates) :", output_text)

    try:
        crop_coordinates = json.loads(output_text)
        print("Crop coordinates (fonction clean coordinates) : ", crop_coordinates)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format. Please check the response.")

    return crop_coordinates
