import json
import math
import pandas as pd


CSV_FILE = "tenue_cahier.csv"  # CSV source
OLD_JSON = "toutes_notes.json"  # JSON actuel (avec les bons commentaires)
NEW_JSON = "toutes_notes_new.json"


# --- helpers -----------------------------------------------------


def parse_number(x):
    """
    Convertit une valeur du CSV en nombre Python :
    - '0,5' -> 0.5
    - '1'   -> 1 (int)
    - NaN ou chaîne vide -> None
    """
    if isinstance(x, str):
        x = x.strip()
        if not x:
            return None
        x = x.replace(",", ".")
        f = float(x)
    elif pd.isna(x):
        return None
    else:
        f = float(x)

    # valeur brute : int si entier, sinon float
    return int(f) if f.is_integer() else f


# --- chargement des données --------------------------------------

# 1) Ancien JSON : on récupère les commentaires déjà reformattés
with open(OLD_JSON, encoding="utf-8") as f:
    old_data = json.load(f)

commentaires_par_prenom = {e["prenom"]: e["commentaire"] for e in old_data}

# 2) CSV des notes
df = pd.read_csv(CSV_FILE)

# On suppose qu'il y a une colonne 'code notation'
if "code notation" not in df.columns:
    raise ValueError("La colonne 'code notation' est introuvable dans le CSV.")

# Liste des codes de sous-notes que l'on veut récupérer
codes_sous_notes = [
    "ce1",
    "ce2",
    "ce3",
    "lu1",
    "lu2",
    "lu3",
    "lu4",
    "lu5",
    "g1",
    "g2",
    "g3",
    "g4",
    "g5",
]

# Les colonnes élèves sont toutes celles après "code notation"
start_idx = df.columns.get_loc("code notation") + 1
student_cols = list(df.columns[start_idx:])

# Mapping nom de colonne CSV -> prénom dans le JSON
csv_to_prenom = {col: col for col in student_cols}
csv_to_prenom["Evann Frank"] = "Evann"  # cas particulier connu


# --- reconstruction des entrées élèves ---------------------------

eleves = []

for csv_col in student_cols:
    prenom = csv_to_prenom.get(csv_col, csv_col)

    entry = {"prenom": prenom}

    # Récupération des sous-notes ce1..g5
    for code in codes_sous_notes:
        # on cherche la ligne où 'code notation' == code
        mask = df["code notation"] == code
        if not mask.any():
            raise ValueError(f"Code de notation '{code}' introuvable dans le CSV.")
        val = df.loc[mask, csv_col].iloc[0]
        entry[code] = parse_number(val)

    # Cas particulier : Tiziri Lin (override demandé)
    if prenom == "Tiziri Lin":
        entry["ce1"] = 1
        entry["ce2"] = 1
        entry["ce3"] = 0.75

    # Calcul de la note = somme des sous-notes
    sous_notes = [entry[c] for c in codes_sous_notes]
    if any(v is None for v in sous_notes):
        raise ValueError(f"Sous-note manquante pour {prenom} : {sous_notes}")

    total = sum(sous_notes)
    entry["note"] = int(total) if float(total).is_integer() else float(total)

    # Ajout du commentaire depuis l'ancien JSON (sans le modifier)
    if prenom in commentaires_par_prenom:
        entry["commentaire"] = commentaires_par_prenom[prenom]
    else:
        # Si jamais un prénom n'existait pas avant : on met un compactitem vide
        entry["commentaire"] = "\\begin{compactitem}\n\\end{compactitem}"

    eleves.append(entry)


# --- écriture du nouveau JSON -----------------------------------

with open(NEW_JSON, "w", encoding="utf-8") as f:
    json.dump(eleves, f, ensure_ascii=False, indent=2)

print("✅ Nouveau JSON généré :", NEW_JSON)
print("Élèves :", [e["prenom"] for e in eleves])
