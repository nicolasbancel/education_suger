import csv
import json
from copy import deepcopy

INPUT_FILE = "notes.json"
OUTPUT_JSON_FILE = "notes_enrichi.json"
OUTPUT_CSV_FILE = "resume_notes_par_classe.csv"

# Mapping prénom + nom -> classe
CLASSES = {
    ("Ysaline", "Bertrand"): "5ème",
    ("Sacha", "Caillet Adam"): "5ème",
    ("Ayaan", "Corazza"): "6ème",
    ("Owen", "Diouf"): "5ème",
    ("Anaëlle", "Duvault"): "6ème",
    ("Charlie", "Esmiol"): "5ème",
    ("Sohantadeo", "Favereau"): "6ème",
    ("Romane", "Lacroix Ferrere"): "6ème",
    ("Mia", "Malpeli"): "6ème",
    ("Evann", "Nguendi Kabiwa"): "6ème",
    ("Inaya", "Njankeu"): "5ème",
    ("Théo", "Otterled"): "5ème",
    ("Alexandre", "Périssé Tremski"): "5ème",
    ("Harrison", "Pick"): "6ème",
    ("Manon", "Remy"): "6ème",
    ("Lila", "Rocher"): "6ème",
    ("Lara", "Samaha"): "5ème",
    ("Fatima", "Sayah"): "5ème",
    ("Adam", "Truchy"): "5ème",
    ("Victoria", "Vannier"): "5ème",
    ("Juan", "Zamora"): "6ème",
}


def compute_note_finale(eleve: dict) -> float:
    notes = [
        eleve["anticipation"]["note"],
        eleve["interaction_teacher"]["note"],
        eleve["attitude_effort"]["note"],
        eleve["formulas_sources"]["note"],
    ]
    moyenne_sur_5 = sum(notes) / 4
    note_sur_20 = moyenne_sur_5 * 4
    return round(note_sur_20, 2)


def add_classe(eleve: dict) -> None:
    key = (eleve.get("prenom", "").strip(), eleve.get("nom", "").strip())
    classe = CLASSES.get(key)
    if classe is None:
        raise KeyError(f"Classe introuvable pour {key[0]} {key[1]}")
    eleve["classe"] = classe


def sort_key(eleve: dict):
    # 6ème d'abord, puis 5ème ; ensuite note décroissante ; puis nom/prénom
    classe_order = {"6ème": 0, "5ème": 1}
    return (
        classe_order.get(eleve.get("classe", ""), 99),
        -float(eleve.get("note_finale", 0)),
        eleve.get("nom", ""),
        eleve.get("prenom", ""),
    )


def format_note_fr(value) -> str:
    """
    Convertit 12.5 -> '12,5' pour un collage facile dans Google Sheets FR.
    Supprime les zéros inutiles : 13.0 -> '13', 12.50 -> '12,5'
    """
    if value is None:
        return ""
    s = f"{float(value):.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = deepcopy(data)
errors = []

# (1) Recalcul / update note finale
# (2) Attribution de la classe
for eleve in new_data:
    try:
        eleve["note_finale"] = compute_note_finale(eleve)  # crée ou remplace
        add_classe(eleve)  # crée ou remplace
    except Exception as e:
        errors.append(f"{eleve.get('prenom', '')} {eleve.get('nom', '')}: {e}")

# Tri pour le JSON enrichi et pour le CSV
sorted_data = sorted(new_data, key=sort_key)

# (3) Création d'une nouvelle version du JSON
with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=2)

# Génération du CSV résumé
# On utilise ; comme séparateur ET des notes avec virgule pour Google Sheets FR
with open(OUTPUT_CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(
        [
            "classe",
            "rang_dans_classe",
            "prenom",
            "nom",
            "note_finale",
            "appreciation_generale",
        ]
    )

    for classe in ["6ème", "5ème"]:
        eleves_classe = [e for e in sorted_data if e.get("classe") == classe]
        for rang, eleve in enumerate(eleves_classe, start=1):
            writer.writerow(
                [
                    eleve.get("classe", ""),
                    rang,
                    eleve.get("prenom", ""),
                    eleve.get("nom", ""),
                    format_note_fr(eleve.get("note_finale", "")),
                    eleve.get("appreciation_generale", ""),
                ]
            )

print(f"JSON enrichi généré : {OUTPUT_JSON_FILE}")
print(f"CSV résumé généré : {OUTPUT_CSV_FILE}")

if errors:
    print("\nErreurs rencontrées :")
    for err in errors:
        print(f"- {err}")
else:
    print("\nTraitement terminé sans erreur.")
