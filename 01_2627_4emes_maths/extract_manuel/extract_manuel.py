#!/usr/bin/env python3
"""Extraction d'un manuel scolaire en ligne (pages JPG) vers un PDF.

Moteur générique : tout ce qui est propre à un manuel donné vit dans un fichier
de configuration JSON (URL, gabarit de nom de fichier, bornes, chapitres).
Pour extraire un autre manuel au même format, on écrit un nouveau JSON.

Usage :
    python3 extract_manuel.py download                 # tout le manuel
    python3 extract_manuel.py download --pages 105-115 # une plage
    python3 extract_manuel.py pdf --sortie pdf/test.pdf
    python3 extract_manuel.py chapitres

Usage personnel de préparation de cours (manuel sous licence acquise).
"""

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RACINE = Path(__file__).resolve().parent
DOSSIER_PAGES = RACINE / "pages"
DOSSIER_PDF = RACINE / "pdf"

# Un CDN qui reçoit 300 requêtes d'un coup n'apprécie pas toujours. 4 connexions
# suffisent largement et restent polies.
CONNEXIONS_PARALLELES = 4
TENTATIVES = 3
NAVIGATEUR = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


# ── Configuration ────────────────────────────────────────────────────────────

def charger_config(chemin):
    with open(chemin, encoding="utf-8") as f:
        cfg = json.load(f)
    for cle in ("base_url", "gabarit", "folio_offset", "page_min", "page_max"):
        if cle not in cfg:
            sys.exit(f"Configuration incomplète : la clé '{cle}' manque dans {chemin}")
    return cfg


def folio_de_page(cfg, page):
    return page + cfg["folio_offset"]


def page_de_folio(cfg, folio):
    return folio - cfg["folio_offset"]


def nom_fichier(cfg, page):
    return cfg["gabarit"].format(page=page, folio=folio_de_page(cfg, page))


# ── Validation des images ────────────────────────────────────────────────────

def jpeg_valide(chemin, cfg=None):
    """Le fichier est-il un vrai JPEG complet ?

    Le CDN répond parfois par une page d'erreur HTML avec un code 200 ; sans ce
    contrôle on se retrouverait avec du HTML enregistré sous une extension .jpg,
    qui ne se verrait qu'au moment de fabriquer le PDF.
    """
    try:
        if chemin.stat().st_size < 1024:
            return False
        with open(chemin, "rb") as f:
            if f.read(2) != b"\xff\xd8":          # signature JPEG
                return False
            f.seek(-2, 2)
            if f.read(2) != b"\xff\xd9":          # marqueur de fin : détecte un fichier tronqué
                return False
    except OSError:
        return False

    if cfg and cfg.get("largeur_attendue"):
        try:
            from PIL import Image
            with Image.open(chemin) as img:
                if img.size != (cfg["largeur_attendue"], cfg["hauteur_attendue"]):
                    print(f"  ! {chemin.name} : {img.size[0]}x{img.size[1]} au lieu de "
                          f"{cfg['largeur_attendue']}x{cfg['hauteur_attendue']}")
        except ImportError:
            pass
        except Exception:
            return False
    return True


# ── Téléchargement ───────────────────────────────────────────────────────────

def telecharger_page(cfg, page):
    """Renvoie (page, statut) avec statut dans {'ok', 'deja', 'echec'}."""
    nom = nom_fichier(cfg, page)
    destination = DOSSIER_PAGES / nom

    if destination.exists() and jpeg_valide(destination):
        return page, "deja"

    url = f"{cfg['base_url']}/{nom}"
    requete = urllib.request.Request(url, headers={"User-Agent": NAVIGATEUR})

    for tentative in range(1, TENTATIVES + 1):
        try:
            with urllib.request.urlopen(requete, timeout=30) as reponse:
                contenu = reponse.read()
            temporaire = destination.with_suffix(".part")
            temporaire.write_bytes(contenu)
            # On ne publie le fichier définitif qu'une fois validé : une interruption
            # en plein téléchargement ne laisse jamais de page corrompue derrière elle.
            if jpeg_valide(temporaire, cfg):
                temporaire.replace(destination)
                return page, "ok"
            temporaire.unlink(missing_ok=True)
            print(f"  ! page {page} : contenu reçu invalide (pas un JPEG complet)")
            return page, "echec"
        except urllib.error.HTTPError as e:
            print(f"  ! page {page} (folio {folio_de_page(cfg, page)}) : HTTP {e.code}")
            return page, "echec"
        except Exception as e:
            if tentative == TENTATIVES:
                print(f"  ! page {page} : {type(e).__name__} après {TENTATIVES} tentatives")
                return page, "echec"
            time.sleep(2 ** tentative)
    return page, "echec"


def commande_download(cfg, args):
    DOSSIER_PAGES.mkdir(exist_ok=True)

    if args.pages:
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", args.pages)
        if not m:
            sys.exit("Format attendu pour --pages : '105-115' ou '106'")
        debut = int(m.group(1))
        fin = int(m.group(2) or m.group(1))
    else:
        debut, fin = cfg["page_min"], cfg["page_max"]

    pages = list(range(debut, fin + 1))
    print(f"{len(pages)} page(s) à traiter : {debut} à {fin} "
          f"(folios {folio_de_page(cfg, debut)} à {folio_de_page(cfg, fin)})\n")

    resultats = {"ok": [], "deja": [], "echec": []}
    with ThreadPoolExecutor(max_workers=CONNEXIONS_PARALLELES) as executeur:
        for i, (page, statut) in enumerate(
            executeur.map(lambda p: telecharger_page(cfg, p), pages), start=1
        ):
            resultats[statut].append(page)
            if statut == "ok" and (i % 25 == 0 or i == len(pages)):
                print(f"  {i}/{len(pages)} pages traitées…")

    print(f"\nTéléchargées : {len(resultats['ok'])}   "
          f"Déjà présentes : {len(resultats['deja'])}   "
          f"Échecs : {len(resultats['echec'])}")
    if resultats["echec"]:
        print("Pages manquantes : " + ", ".join(str(p) for p in resultats["echec"]))
        return 1
    return 0


# ── Fabrication des PDF ──────────────────────────────────────────────────────

def pages_disponibles(cfg, folio_debut=None, folio_fin=None):
    """Chemins des JPG présents, triés par numéro de page croissant."""
    debut = page_de_folio(cfg, folio_debut) if folio_debut else cfg["page_min"]
    fin = page_de_folio(cfg, folio_fin) if folio_fin else cfg["page_max"]
    chemins = []
    for page in range(debut, fin + 1):
        chemin = DOSSIER_PAGES / nom_fichier(cfg, page)
        if chemin.exists():
            chemins.append(chemin)
    return chemins


def fabriquer_pdf(chemins, sortie):
    """Assemble des JPG en PDF sans les réencoder (qualité identique à la source)."""
    try:
        import img2pdf
    except ImportError:
        sys.exit("img2pdf est absent. Installer avec :  pip3 install --user img2pdf")

    sortie.parent.mkdir(parents=True, exist_ok=True)
    with open(sortie, "wb") as f:
        f.write(img2pdf.convert([str(c) for c in chemins]))
    poids = sortie.stat().st_size / 1024 / 1024
    print(f"  {sortie.relative_to(RACINE)} — {len(chemins)} pages, {poids:.1f} Mo")


def commande_pdf(cfg, args):
    chemins = pages_disponibles(cfg)
    if not chemins:
        sys.exit(f"Aucune image dans {DOSSIER_PAGES}. Lancer 'download' d'abord.")
    sortie = Path(args.sortie) if args.sortie else DOSSIER_PDF / "manuel_complet.pdf"
    if not sortie.is_absolute():
        sortie = RACINE / sortie
    fabriquer_pdf(chemins, sortie)
    return 0


def ardoise(texte):
    """Transforme un titre de chapitre en nom de fichier sans accent ni espace."""
    sans_accent = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", sans_accent.lower()).strip("_")[:60]


def commande_chapitres(cfg, args):
    chapitres = cfg.get("chapitres") or []
    if not chapitres:
        sys.exit("Aucun chapitre dans la configuration. Remplir la clé 'chapitres' "
                 "du JSON (num, titre, folio_debut, folio_fin).")
    DOSSIER_PDF.mkdir(exist_ok=True)
    for ch in chapitres:
        chemins = pages_disponibles(cfg, ch["folio_debut"], ch["folio_fin"])
        if not chemins:
            print(f"  ! chapitre {ch['num']} : aucune page téléchargée, ignoré")
            continue
        sortie = DOSSIER_PDF / f"ch{ch['num']:02d}_{ardoise(ch['titre'])}.pdf"
        fabriquer_pdf(chemins, sortie)
    return 0


# ── Point d'entrée ───────────────────────────────────────────────────────────

def main():
    parseur = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parseur.add_argument("--config", default=str(RACINE / "manuel_4eme.json"),
                         help="fichier de configuration JSON du manuel")
    sous = parseur.add_subparsers(dest="commande", required=True)

    p_dl = sous.add_parser("download", help="télécharger les pages")
    p_dl.add_argument("--pages", help="plage de pages, ex. 105-115 (défaut : tout)")

    p_pdf = sous.add_parser("pdf", help="assembler toutes les pages en un PDF")
    p_pdf.add_argument("--sortie", help="chemin du PDF produit")

    sous.add_parser("chapitres", help="produire un PDF par chapitre")

    args = parseur.parse_args()
    cfg = charger_config(args.config)

    return {
        "download": commande_download,
        "pdf": commande_pdf,
        "chapitres": commande_chapitres,
    }[args.commande](cfg, args)


if __name__ == "__main__":
    sys.exit(main())
