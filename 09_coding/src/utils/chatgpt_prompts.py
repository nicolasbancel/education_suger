# filepath: src/utils/chatgpt_prompts.py
from openai import OpenAI
#from config.settings import OPENAI_API_KEY
import sys
import base64
import os
import json
from pydantic import BaseModel
from typing import List

class Exercice_Coordinates(BaseModel):
    top_left: List[str]
    bottom_right: List[str]

#openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

print(os.environ.get("OPENAI_API_KEY"))

# Documentation on how to extract the image 
# https://platform.openai.com/docs/guides/images-vision?api-mode=responses&format=base64-encoded

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_crop_coordinates(image_path, exercise_number):
    """
    Sends a description of the image to ChatGPT to identify crop coordinates.
    """
    #with open(image_path, "rb") as image_file:
    #    image_data = image_file.read()
    # files = {"file": ("image.jpg", image_data, "image/jpg")}
    
    base64_image = encode_image(image_path)
    
    prompt_1 = (f"Étant donné le fichier image suivant et le numéro de l'exercice {exercise_number}, "
    f"identifie les coordonnées en pixels des coins à découper qui délimitent l'exercice sur la page."
    f"Le format attendu est un dictionnaire JSON avec les clés 'top_left' et 'bottom_right',"
    f"{{'top_left': [x1, y1], 'bottom_right': [x2, y2]}}."
    )
    
    prompt_2 = (
    f"Tu es un modèle de vision artificielle. On te fournit une image scannée d'une feuille d'exercice, "
    f"et on te demande de localiser précisément l'exercice numéro {exercise_number} sur la page. "
    "Donne les coordonnées en pixels des coins opposés de la boîte qui encadre entièrement cet exercice. "
    "Réponds uniquement avec un objet JSON de la forme :\n"
    "{'top_left': [x1, y1], 'bottom_right': [x2, y2]}\n"
    "Les coordonnées doivent être des entiers positifs. Ne propose aucune explication ou conseil, uniquement l'objet JSON."
)
    
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Tu es un assistant vision IA très précis. Tes réponses sont uniquement en JSON."
            },
            {
            "role": "user",
            "content":[
                {"type":"input_text", "text": prompt_2},
                {
                    "type":"input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }]
        }],
        #response_format=Exercice_Coordinates,
        # response_format="json",
        #{"type": "json_object"}
    )
    print("Response: ", response)
    try:
        output_text = response.output[0].content[0].text
        print("Output_text: ", output_text)
    except:
        output_text = None
        raise ValueError("Invalid response format. Expected JSON with 'top_left' and 'bottom_right' keys.")
    return output_text
#response['choices'][0]['message']['content']

def clean_coordinates(text):
    key_0 = Exercice_Coordinates.model_json_schema()['required'][0]
    key_1 = Exercice_Coordinates.model_json_schema()['required'][1]
    key_0_type = Exercice_Coordinates.model_json_schema()['properties'][key_0]['type']
    key_1_type = Exercice_Coordinates.model_json_schema()['properties'][key_1]['type']
    prompt = (f"Tu es un modèle spécialisé dans le fait de générer des dictionnaires JSON à partir d'un format texte."
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
                "content": "Tu es une IA qui convertit des données en JSON. Tes réponses sont uniquement en JSON."
            },
            {
            "role": "user",
            "content":[
                {"type":"input_text", "text": prompt},
  ]
        }],
    )
    output_text = response.output[0].content[0].text
    print("Output text (fonction clean coordinates) :", output_text)
    
    try:
        crop_coordinates = json.loads(output_text)
        print("Crop coordinates (fonction clean coordinates) : ", crop_coordinates)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format. Please check the response.")
    
    return crop_coordinates


def get_correction(exercise_text):
    """
    Sends the exercise text to ChatGPT to generate a correction.
    """
    prompt = f"Provide a detailed correction for the following exercise: {exercise_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    
# /Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg
# 20

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


    """
    exercise_text = input("Enter the exercise text for correction: ")
    try:
        correction = get_correction(exercise_text)
        print("Correction:", correction)
    except Exception as e:
        print("Error getting correction:", e)
    """
