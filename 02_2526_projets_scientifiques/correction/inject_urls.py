# -*- coding: utf-8 -*-
"""
Injecte les URLs Google Sheets depuis le CSV dans le JSON des notes.
Valide le format des URLs et le matching prénom+nom.
Écrit le résultat dans notes_v3.json.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata

CSV_FILE = "scientific_projects_summary_urls.csv"
JSON_IN = "notes_v2.json"
JSON_OUT = "notes_v3.json"

GSHEET_URL_PATTERN = re.compile(
    r"^https://docs\.google\.com/spreadsheets/d/[a-zA-Z0-9_-]+/edit[?#].*gid=\d+"
)


def normalize(s: str) -> str:
    """Minuscule + suppression accents pour comparaison souple."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def validate_url(url: str, context: str) -> list[str]:
    """Vérifie le format d'une URL Google Sheets. Retourne liste d'erreurs."""
    errors = []
    if not url or not url.strip():
        errors.append(f"  URL vide pour {context}")
    elif not GSHEET_URL_PATTERN.match(url.strip()):
        errors.append(f"  URL invalide pour {context}: {url[:80]}...")
    return errors


# --- Chargement ---
with open(CSV_FILE, encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))

with open(JSON_IN, encoding="utf-8") as f:
    eleves = json.load(f)

# --- Index JSON par (prenom_norm, nom_norm) ---
eleve_index: dict[tuple[str, str], dict] = {}
for e in eleves:
    key = (normalize(e["prenom"]), normalize(e["nom"]))
    eleve_index[key] = e

# --- Matching + injection ---
all_errors: list[str] = []
matched = 0
csv_keys_seen = set()

for row in csv_rows:
    prenom = row["prenom"].strip()
    nom = row["nom"].strip()
    key = (normalize(prenom), normalize(nom))
    csv_keys_seen.add(key)

    if key not in eleve_index:
        all_errors.append(f"CSV: {prenom} {nom} → pas trouvé dans le JSON")
        continue

    url_objects = row["url_objects"].strip()
    url_distances = row["url_distances"].strip()
    url_transport = row["url_transport"].strip()

    # Validation format
    ctx = f"{prenom} {nom}"
    all_errors.extend(validate_url(url_objects, f"{ctx} / objects"))
    all_errors.extend(validate_url(url_distances, f"{ctx} / distances"))
    all_errors.extend(validate_url(url_transport, f"{ctx} / transport"))

    # Injection
    eleve_index[key]["google_sheets"] = {
        "objects_inventory": {
            "label": f"[{prenom}] Carbon Footprint",
            "url": url_objects,
        },
        "transport_distances": {
            "label": f"[{prenom}] Distances",
            "url": url_distances,
        },
        "transport_carbon": {
            "label": f"[{prenom}] Transport Carbon Footprint",
            "url": url_transport,
        },
    }
    matched += 1

# --- Élèves JSON sans URL ---
json_keys = set(eleve_index.keys())
missing_in_csv = json_keys - csv_keys_seen
for key in sorted(missing_in_csv):
    e = eleve_index[key]
    all_errors.append(f"JSON: {e['prenom']} {e['nom']} → pas de ligne dans le CSV")

# --- Rapport ---
print(f"\n{'='*50}")
print(f"Élèves dans le JSON : {len(eleves)}")
print(f"Lignes dans le CSV  : {len(csv_rows)}")
print(f"Matchés avec succès : {matched}")
print(f"URLs totales        : {matched * 3}")

if all_errors:
    print(f"\n⚠️  {len(all_errors)} problème(s) détecté(s) :")
    for err in all_errors:
        print(f"  • {err}")
else:
    print("\n✅ Aucune erreur détectée.")

# --- Écriture ---
with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(eleves, f, ensure_ascii=False, indent=2)

print(f"\n✅ Fichier écrit : {JSON_OUT}")
