from __future__ import annotations
"""
Client pour l'API EcoleDirecte (reverse-engineered).

AVERTISSEMENT : Il n'existe pas d'API officielle publique.
Les endpoints peuvent changer sans préavis.

Authentification (validée 2025) :
  1. GET  /v3/login.awp?gtk=1&v=4.96.1  → cookie GTK
  2. POST /v3/login.awp?v=4.96.1        → header X-GTK + credentials → token

Deux domaines distincts (observés en 2025) :
  - api.ecoledirecte.com   → authentification uniquement
  - apip.ecoledirecte.com  → toutes les données (classes, élèves, bulletins…)
"""
import json
import httpx
import logging
from typing import List, Optional
from urllib.parse import quote

logger = logging.getLogger(__name__)

AUTH_BASE_URL = "https://api.ecoledirecte.com/v3"   # login uniquement
DATA_BASE_URL = "https://apip.ecoledirecte.com/v3"  # données
API_VERSION = "4.96.1"

# Headers communs qui imitent Chrome macOS
_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.ecoledirecte.com",
    "Referer": "https://www.ecoledirecte.com/",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}


class EcoleDirecteError(Exception):
    pass


class EcoleDirecteClient:
    def __init__(self):
        self._client = httpx.Client(
            headers=_BROWSER_HEADERS,
            timeout=30.0,
        )

    def _encode(self, payload: dict) -> bytes:
        """Encode un dict en format `data=<urlencoded_json>` attendu par l'API."""
        return f"data={quote(json.dumps(payload, separators=(',', ':'), ensure_ascii=False))}".encode()

    def _post(self, path: str, payload: dict, token: Optional[str] = None, base_url: str = DATA_BASE_URL) -> dict:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if token:
            headers["X-Token"] = token
        response = self._client.post(
            f"{base_url}{path}",
            content=self._encode(payload),
            headers=headers,
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise EcoleDirecteError(
                f"EcoleDirecte HTTP {e.response.status_code} sur {path} : {e.response.text[:200]}"
            )
        data = response.json()
        if data.get("code") not in (200, 201):
            raise EcoleDirecteError(
                f"EcoleDirecte error {data.get('code')} : {data.get('message', 'Erreur inconnue')}"
            )
        return data

    def _get_gtk(self) -> str:
        """
        Récupère le token GTK (cookie) requis avant le login.
        Le cookie est nommé 'GTK' (majuscules).
        """
        response = self._client.get(f"{AUTH_BASE_URL}/login.awp?gtk=1&v={API_VERSION}")
        return response.cookies.get("GTK", "")

    def login(self, username: str, password: str) -> dict:
        """
        Authentification en deux étapes (validée 2025).
        Retourne {"token": str, "account_id": int, "name": str}.
        """
        gtk = self._get_gtk()

        login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if gtk:
            login_headers["X-GTK"] = gtk

        response = self._client.post(
            f"{AUTH_BASE_URL}/login.awp?v={API_VERSION}",
            content=self._encode({
                "identifiant": username,
                "motdepasse": password,
                "isReLogin": False,
                "uuid": "",
                "fa": [],
            }),
            headers=login_headers,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") not in (200, 201):
            raise EcoleDirecteError(
                f"EcoleDirecte error {data.get('code')} : {data.get('message', 'Erreur inconnue')}"
            )

        token = data["token"]
        accounts = data["data"]["accounts"]
        account = next(
            (a for a in accounts if a.get("typeCompte") == "P"),
            accounts[0],
        )
        account_id = account["id"]
        name = f"{account.get('prenom', '')} {account.get('nom', '')}".strip()

        # Les classes sont dans profile.classes (pas besoin d'un appel séparé)
        profile_classes = account.get("profile", {}).get("classes", [])
        classes = [
            {
                "id": str(c["id"]),
                "name": c.get("libelle", c.get("code", str(c["id"]))),
                "annee_scolaire": c.get("anneeScolaire", ""),
            }
            for c in profile_classes
        ]
        logger.info(f"ED login OK : id={account_id}, name={name}, classes={[c['name'] for c in classes]}")
        return {
            "token": token,
            "account_id": account_id,
            "name": name,
            "classes": classes,
        }

    def get_classes(self, token: str, enseignant_id: int) -> List[dict]:
        """Récupère les classes de l'enseignant."""
        data = self._post(
            f"/enseignants/{enseignant_id}/classes.awp?verbe=get&v={API_VERSION}",
            {},
            token=token,
        )
        classes = data.get("data", [])
        return [
            {
                "id": str(c["id"]),
                "name": c.get("libelle", c.get("name", str(c["id"]))),
                "annee_scolaire": c.get("anneeScolaire", ""),
            }
            for c in classes
        ]

    def get_students(self, token: str, classe_id: str) -> List[dict]:
        """Récupère les élèves d'une classe."""
        data = self._post(
            f"/classes/{classe_id}/eleves.awp?verbe=get&v={API_VERSION}",
            {},
            token=token,
        )
        eleves = data.get("data", {}).get("eleves", data.get("data", []))
        return [
            {
                "id": e["id"],
                "first_name": e.get("prenom", ""),
                "last_name": e.get("nom", ""),
            }
            for e in eleves
        ]

    def get_student_notes(self, token: str, eleve_id: int, annee_scolaire: str = "") -> dict:
        """
        Récupère les notes et appréciations d'un élève pour toutes les périodes.
        Retourne le dict 'data' complet (clés: periodes, notes, parametrage...).
        Chaque période (A001=T1, A002=T2, A003=T3) contient:
          - ensembleMatieres.moyenneGenerale
          - ensembleMatieres.appreciationPP  (appréciation du professeur principal)
          - ensembleMatieres.decisionDuConseil
          - ensembleMatieres.disciplines[]  (par matière: discipline, moyenne, appreciationProfesseur)
        """
        data = self._post(
            f"/eleves/{eleve_id}/notes.awp?verbe=get&v={API_VERSION}",
            {"anneeScolaire": annee_scolaire},
            token=token,
        )
        return data.get("data", {})

    def get_student_vie_scolaire(self, token: str, eleve_id: int) -> dict:
        """
        Récupère la vie scolaire d'un élève (absences, retards, sanctions...).
        """
        data = self._post(
            f"/eleves/{eleve_id}/viescolaire.awp?verbe=get&v={API_VERSION}",
            {},
            token=token,
        )
        return data.get("data", {})

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
