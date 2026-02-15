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
    api_key=os.environ.get("OPENAI_API_KEY_CHRIS")
)

system_prompt = "A chaque message / réponse que tu écris, je veux que tu commences par une phrase avec ces mots : J'AI TRES ENVIE DE FAIRE CACA. Et tu écriras ces mots en majuscule. Le reste de ton message peut être en minuscule"
user_content = "Rédige un post LinkedIn en français à propos de l'actualité puis inclue un message promotionnel sur mes formations sur le no code"

response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ],
)

text_final = response.output[0].content[0].text.strip()

print(text_final)

response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "user", "content": user_content},
    ],
)
