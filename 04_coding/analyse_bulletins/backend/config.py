"""
Configuration de l'année scolaire.
Modifiez les dates ici pour filtrer les absences/retards/sanctions par trimestre.
Format des dates : "AAAA-MM-JJ"
"""
from __future__ import annotations

# Dates de début et de fin de chaque trimestre
# Ces dates sont utilisées pour filtrer les événements vie scolaire affichés
# dans la fiche d'un élève.
TRIMESTRES_DATES = {
    1: {"debut": "2025-09-02", "fin": "2025-12-19"},
    2: {"debut": "2026-01-05", "fin": "2026-03-27"},
    3: {"debut": "2026-04-06", "fin": "2026-07-04"},
}
