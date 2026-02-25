from __future__ import annotations
"""
Service LLM — génération d'appréciations et de recommandations de récompense via OpenAI.
"""
import os
import json
from typing import Optional, List
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o"

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
{student_data}
{evolution_section}"""


# ─── Extraction factuelle ──────────────────────────────────────────────────────

def extract_bulletin_data(bulletin_text: str) -> List[dict]:
    """
    Mode extraction : retourne les lignes structurées du bulletin.
    Lève une ValueError si le JSON retourné est invalide.
    """
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM},
            {"role": "user", "content": EXTRACTION_USER_TEMPLATE.format(bulletin_text=bulletin_text)},
        ],
    )
    raw = response.choices[0].message.content.strip()
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


def _format_evolution(current_lines: List[dict], prev_data: dict) -> str:
    """
    Construit la section 'évolution' comparant T_prev et T_current matière par matière.
    """
    prev_t = prev_data["trimestre"]
    curr_t = prev_t + 1
    prev_by_subject = {l["matiere"]: l for l in prev_data["lines"]}

    lines = [f"\nCONTEXTE TRIMESTRE PRÉCÉDENT (T{prev_t}) :"]

    if prev_data.get("mention"):
        lines.append(f"Mention T{prev_t} : {prev_data['mention']}")
    if prev_data.get("appreciation_generale"):
        lines.append(f"Appréciation générale T{prev_t} : {prev_data['appreciation_generale']}")

    lines.append(f"\nÉvolution des moyennes par matière (T{prev_t} → T{curr_t}) :")
    for line in current_lines:
        matiere = line["matiere"]
        if matiere == "BILAN":
            continue
        curr_moy = line.get("moyenne")
        prev_line = prev_by_subject.get(matiere)
        prev_moy = prev_line["moyenne"] if prev_line else None

        if curr_moy is not None and prev_moy is not None:
            delta = curr_moy - prev_moy
            sign = "+" if delta >= 0 else ""
            evolution = f"T{prev_t}={prev_moy} → T{curr_t}={curr_moy} ({sign}{delta:.2f})"
        elif curr_moy is not None:
            evolution = f"T{curr_t}={curr_moy} (pas de donnée T{prev_t})"
        else:
            continue

        prev_appre = prev_line["appreciation"] if prev_line and prev_line.get("appreciation") else None
        appre_str = f' | appréciation T{prev_t}: "{prev_appre}"' if prev_appre else ""
        lines.append(f"- {matiere} : {evolution}{appre_str}")

    return "\n".join(lines)


def generate_student_output(
    prenom: str,
    nom: str,
    trimestre: int,
    bulletin_lines: List[dict],
    custom_prompt: Optional[str] = None,
    prev_data: Optional[dict] = None,
) -> dict:
    """
    Mode génération : retourne appréciation, synthèse et suggestion de récompense.
    Inclut l'évolution par rapport au trimestre précédent si prev_data est fourni.
    """
    instructions = custom_prompt or DEFAULT_GENERATION_PROMPT

    lines_parts = []
    for line in bulletin_lines:
        parts = [f"- {line['matiere']}"]
        if line.get('moyenne') is not None:
            cls = f" (classe: {line['moyenne_classe']})" if line.get('moyenne_classe') else ""
            rang = f" rang {line['rang']}" if line.get('rang') else ""
            parts.append(f"moy={line['moyenne']}{cls}{rang}")
        if line.get('appreciation'):
            parts.append(f"appréciation: {line['appreciation']}")
        if line.get('contenu'):
            parts.append(f"contenu: {line['contenu']}")
        if line.get('absences'):
            parts.append(f"absences={line['absences']}, retards={line.get('retards', 0)}")
        lines_parts.append(" | ".join(parts))
    student_data_str = "\n".join(lines_parts)

    evolution_section = _format_evolution(bulletin_lines, prev_data) if prev_data else ""

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": GENERATION_SYSTEM},
            {
                "role": "user",
                "content": GENERATION_USER_TEMPLATE.format(
                    prenom=prenom,
                    nom=nom,
                    trimestre=trimestre,
                    custom_instructions=instructions,
                    student_data=student_data_str,
                    evolution_section=evolution_section,
                ),
            },
        ],
    )
    raw = response.choices[0].message.content.strip()
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
