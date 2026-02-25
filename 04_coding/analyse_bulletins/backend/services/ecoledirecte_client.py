"""
Client pour l'API EcoleDirecte (reverse-engineered).

AVERTISSEMENT : Il n'existe pas d'API officielle publique.
Ce client est basé sur la documentation communautaire :
  https://github.com/EduWireApps/ecoledirecte-api-docs

Les endpoints peuvent changer sans préavis. En cas d'échec,
vérifier la doc communautaire et ajuster les routes.
"""
import json
import httpx
from typing import Optional
from urllib.parse import quote

BASE_URL = "https://api.ecoledirecte.com/v3"

# Délai entre requêtes successives pour éviter le rate-limiting
REQUEST_DELAY_SECONDS = 1.0


class EcoleDirecteError(Exception):
    pass


class EcoleDirecteClient:
    def __init__(self):
        self._client = httpx.Client(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            timeout=30.0,
        )

    def _encode(self, payload: dict) -> str:
        """Encode un dict en format `data=<urlencoded_json>` attendu par l'API."""
        return f"data={quote(json.dumps(payload))}"

    def _post(self, path: str, payload: dict, token: Optional[str] = None) -> dict:
        headers = {}
        if token:
            headers["X-Token"] = token
        response = self._client.post(
            f"{BASE_URL}{path}",
            content=self._encode(payload),
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") not in (200, 201):
            raise EcoleDirecteError(
                f"EcoleDirecte error {data.get('code')} : {data.get('message', 'Erreur inconnue')}"
            )
        return data

    def login(self, username: str, password: str) -> dict:
        """
        Authentification. Retourne {"token": str, "account_id": int, "name": str}.
        """
        data = self._post(
            "/login.awp?v=4",
            {
                "identifiant": username,
                "motdepasse": password,
                "isReLogin": False,
                "uuid": "",
                "fa": [],
            },
        )
        token = data["token"]
        accounts = data["data"]["accounts"]

        # Priorité au compte enseignant (typeCompte == "P")
        account = next(
            (a for a in accounts if a.get("typeCompte") == "P"),
            accounts[0],
        )
        return {
            "token": token,
            "account_id": account["id"],
            "name": f"{account.get('prenom', '')} {account.get('nom', '')}".strip(),
        }

    def get_classes(self, token: str, enseignant_id: int) -> list[dict]:
        """
        Récupère les classes de l'enseignant.
        Retourne une liste de {"id": str, "name": str, "annee_scolaire": str}.
        """
        data = self._post(
            f"/enseignants/{enseignant_id}/classes.awp?verbe=get&v=4",
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

    def get_students(self, token: str, classe_id: str) -> list[dict]:
        """
        Récupère les élèves d'une classe.
        Retourne une liste de {"id": int, "first_name": str, "last_name": str}.
        """
        data = self._post(
            f"/classes/{classe_id}/eleves.awp?verbe=get&v=4",
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

    def download_bulletin_pdf(
        self, token: str, eleve_id: int, trimestre: int, annee_scolaire: str = ""
    ) -> bytes:
        """
        Télécharge le bulletin PDF d'un élève pour un trimestre donné.

        NOTE : Endpoint incertain — les versions de l'API varient.
        idPeriode : "A001" = trimestre 1, "A002" = T2, "A003" = T3.
        Si cet endpoint échoue, vérifier :
          https://github.com/EduWireApps/ecoledirecte-api-docs
        """
        periode_id = f"A00{trimestre}"

        response = self._client.post(
            f"{BASE_URL}/eleves/{eleve_id}/donneesbulletins.awp?verbe=get&v=4",
            content=self._encode(
                {"anneeScolaire": annee_scolaire, "idPeriode": periode_id}
            ),
            headers={"X-Token": token},
        )
        response.raise_for_status()

        # Si la réponse est un PDF directement
        if "application/pdf" in response.headers.get("content-type", ""):
            return response.content

        # Sinon, chercher un lien vers le PDF dans la réponse JSON
        data = response.json()
        if data.get("code") not in (200, 201):
            raise EcoleDirecteError(
                f"Impossible de récupérer le bulletin : {data.get('message')}"
            )

        # Chercher l'URL du PDF dans la réponse (structure variable selon les versions)
        pdf_url = (
            data.get("data", {}).get("url")
            or data.get("data", {}).get("fichier", {}).get("url")
        )
        if pdf_url:
            pdf_response = self._client.get(pdf_url, headers={"X-Token": token})
            pdf_response.raise_for_status()
            return pdf_response.content

        raise EcoleDirecteError(
            f"Format de réponse bulletin inattendu pour l'élève {eleve_id}, trimestre {trimestre}. "
            "Vérifier la documentation de l'API EcoleDirecte."
        )

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
