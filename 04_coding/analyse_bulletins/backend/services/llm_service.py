from __future__ import annotations
"""
Service LLM — deux modes distincts :
  - Mode extraction  : sortie factuelle stricte (équivalent du bulletin)
  - Mode génération  : appréciation / synthèse / récompense configurable par le professeur
"""
import os
import json
from typing import Optional, List
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-6"

# ─── Prompts par défaut ────────────────────────────────────────────────────────

EXTRACTION_SYSTEM = """Tu es un assistant d'extraction de données scolaires.
Ta seule tâche est d'extraire les informations FACTUELLES du bulletin fourni.
Règles absolues :
- Aucune interprétation, aucune reformulation
- Si une donnée est absente du bulletin → champ null
- Retourner UNIQUEMENT un JSON valide, sans markdown, sans commentaire"""

EXTRACTION_USER_TEMPLATE = """Extrait les données du bulletin suivant.

Format de sortie (JSON strict) :
{{
  "lignes": [
    {{
      "matiere": "string",
      "appreciation": "string ou null",
      "moyenne": "number ou null",
      "absences": "integer ou null",
      "retards": "integer ou null"
    }}
  ]
}}

BULLETIN :
{bulletin_text}"""

GENERATION_SYSTEM = """Tu es un professeur principal expérimenté.
Tu rédiges des appréciations de conseil de classe à partir de données de bulletins.
Règles :
- Basé UNIQUEMENT sur les données fournies
- Pas d'hallucination : si tu n'es pas certain, indique-le
- Retourner UNIQUEMENT un JSON valide, sans markdown"""

GENERATION_USER_TEMPLATE = """Rédige pour l'élève {prenom} {nom} les trois éléments suivants.

Format de sortie (JSON strict) :
{{
  "appreciation_generale": "string (3-4 phrases)",
  "synthese": "string (points forts / axes d'amélioration / alertes)",
  "suggestion_recompense": "Félicitations | Tableau d'honneur | Encouragements | Mention neutre | Aucune"
}}

{custom_instructions}

DONNÉES DE L'ÉLÈVE (trimestre {trimestre}) :
{student_data}"""


# ─── Extraction factuelle ──────────────────────────────────────────────────────

def extract_bulletin_data(bulletin_text: str) -> List[dict]:
    """
    Mode extraction : retourne les lignes structurées du bulletin.
    Lève une ValueError si le JSON retourné est invalide.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=EXTRACTION_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": EXTRACTION_USER_TEMPLATE.format(bulletin_text=bulletin_text),
            }
        ],
    )
    raw = response.content[0].text.strip()
    try:
        result = json.loads(raw)
        return result.get("lignes", [])
    except json.JSONDecodeError as e:
        raise ValueError(f"Réponse LLM non-JSON : {raw[:200]}") from e


# ─── Génération synthétique ────────────────────────────────────────────────────

DEFAULT_GENERATION_PROMPT = """Instructions supplémentaires :
- Ton professionnel mais bienveillant
- Longueur : concis (3-4 phrases pour l'appréciation, 2-3 points pour la synthèse)
- Vocabulaire adapté au niveau collège/lycée"""


def generate_student_output(
    prenom: str,
    nom: str,
    trimestre: int,
    bulletin_lines: List[dict],
    custom_prompt: Optional[str] = None,
) -> dict:
    """
    Mode génération : retourne appréciation, synthèse et suggestion de récompense.
    """
    instructions = custom_prompt or DEFAULT_GENERATION_PROMPT

    student_data_str = "\n".join(
        f"- {line['matiere']} : moy={line.get('moyenne', 'N/A')}, "
        f"appréciation='{line.get('appreciation', '')}', "
        f"absences={line.get('absences', 0)}, retards={line.get('retards', 0)}"
        for line in bulletin_lines
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=GENERATION_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": GENERATION_USER_TEMPLATE.format(
                    prenom=prenom,
                    nom=nom,
                    trimestre=trimestre,
                    custom_instructions=instructions,
                    student_data=student_data_str,
                ),
            }
        ],
    )
    raw = response.content[0].text.strip()
    try:
        result = json.loads(raw)
        return {
            "general_appreciation": result.get("appreciation_generale"),
            "synthesis": result.get("synthese"),
            "reward_suggestion": result.get("suggestion_recompense"),
        }
    except json.JSONDecodeError as e:
        raise ValueError(f"Réponse LLM non-JSON : {raw[:200]}") from e


def get_default_generation_prompt() -> str:
    return DEFAULT_GENERATION_PROMPT
