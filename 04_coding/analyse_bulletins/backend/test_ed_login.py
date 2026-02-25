"""
Script de diagnostic pour tester la connexion EcoleDirecte.
Usage : .venv/bin/python test_ed_login.py
"""

import json
import httpx
from urllib.parse import quote

LOGIN = input("Identifiant EcoleDirecte : ")
PASSWORD = input("Mot de passe : ")

API_VERSION = "4.96.1"
BASE_URL = "https://api.ecoledirecte.com/v3"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.ecoledirecte.com/",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}

with httpx.Client(timeout=15.0, headers=HEADERS) as client:

    # Étape 1 : GET gtk
    print("\n--- Étape 1 : récupération GTK ---")
    gtk_resp = client.get(f"{BASE_URL}/login.awp?gtk=1&v={API_VERSION}")
    print(f"HTTP status : {gtk_resp.status_code}")
    print(f"Cookies : {dict(gtk_resp.cookies)}")
    print(f"Réponse body : {gtk_resp.text[:500]}")

    # Chercher le GTK dans cookies ET dans le body JSON
    gtk = gtk_resp.cookies.get("gtk", "") or gtk_resp.cookies.get("GTK", "")
    if not gtk:
        try:
            body = gtk_resp.json()
            gtk = body.get("gtk", "") or body.get("GTK", "") or body.get("token", "")
            print(f"GTK dans JSON : {gtk!r}")
        except Exception:
            pass
    print(f"GTK final utilisé : {gtk[:40]!r}..." if gtk else "GTK : vide")

    # Étape 2 : POST login
    print("\n--- Étape 2 : login ---")
    payload = {
        "identifiant": LOGIN,
        "motdepasse": PASSWORD,
        "isReLogin": False,
        "uuid": "",
        "fa": [],
    }
    body = (
        f"data={quote(json.dumps(payload, separators=(',', ':'), ensure_ascii=False))}"
    )

    extra = {"Content-Type": "application/x-www-form-urlencoded"}
    if gtk:
        extra["X-GTK"] = gtk

    resp = client.post(
        f"{BASE_URL}/login.awp?v={API_VERSION}",
        content=body.encode(),
        headers=extra,
    )
    print(f"HTTP status : {resp.status_code}")
    try:
        data = resp.json()
        print(f"Code ED : {data.get('code')}")
        print(f"Message : {data.get('message')}")
        if data.get("code") == 200:
            token = data.get("token", "")
            print(f"\nConnexion reussie !")
            print(f"Token : {token[:40]}...")
            for a in data.get("data", {}).get("accounts", []):
                print(
                    f"  Compte : {a.get('typeCompte')} — {a.get('prenom')} {a.get('nom')}"
                )
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
    except Exception:
        print(f"Body brut : {resp.text[:300]}")
