#!/usr/bin/env python3
"""Extraction d'un manuel scolaire en ligne (pages JPG) vers un PDF.

Moteur générique : tout ce qui est propre à un manuel donné vit dans un fichier
de configuration JSON (URL, gabarit de nom de fichier, bornes, chapitres).
Pour extraire un autre manuel au même format, on écrit un nouveau JSON.

Usage courant :
    python3 extract_manuel.py download                  # telecharge les pages
    python3 extract_manuel.py pdf --purge               # assemble, puis efface les JPG
    python3 extract_manuel.py chapitres                 # decoupe un PDF par chapitre
    python3 extract_manuel.py extraire 102 103          # ressort des pages en JPG

Aucune etape ne reencode quoi que ce soit : le JPG d'origine est recopie tel quel
dans le PDF (/DCTDecode), et 'extraire' le ressort octet pour octet. C'est ce qui
permet a 'pdf --purge' d'effacer les JPG sans rien perdre — il ne le fait
d'ailleurs qu'apres avoir compare les empreintes MD5 une a une.

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

def page_de_nom(cfg, chemin):
    """Numero de page lu dans le nom du fichier (pages-0106-folio-102.jpg -> 106)."""
    return int(re.search(r"pages-(\d+)", chemin.name).group(1))


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
    # outputstream : img2pdf ecrit directement dans le fichier au lieu de construire
    # tout le PDF en memoire (sur 304 pages, cela evite un pic de ~400 Mo de RAM).
    with open(sortie, "wb") as f:
        img2pdf.convert([str(c) for c in chemins], outputstream=f)
    poids = sortie.stat().st_size / 1024 / 1024
    print(f"  {sortie.relative_to(RACINE)} — {len(chemins)} pages, {poids:.1f} Mo")


def verifier_pdf(pdf, chemins):
    """Chaque JPG est-il present dans le PDF, octet pour octet ?

    C'est le feu vert avant toute suppression : on ne se fie pas au fait que le
    PDF "a l'air" correct, on compare les empreintes MD5 du fichier source et du
    flux image reellement stocke dans le PDF. Tant que ce n'est pas verifie, les
    originaux restent sur le disque.
    """
    import hashlib
    import pikepdf

    with pikepdf.open(pdf) as doc:
        if len(doc.pages) != len(chemins):
            print(f"  ! {len(doc.pages)} pages dans le PDF pour {len(chemins)} images")
            return False
        for page, chemin in zip(doc.pages, chemins):
            images = list(page.images.values())
            if len(images) != 1:
                print(f"  ! {chemin.name} : {len(images)} images dans la page du PDF")
                return False
            if hashlib.md5(images[0].read_raw_bytes()).digest() != \
               hashlib.md5(chemin.read_bytes()).digest():
                print(f"  ! {chemin.name} : les octets du PDF different de l'original")
                return False
    return True


def poser_folios(pdf, folio_initial):
    """Inscrit la numerotation du manuel dans le PDF.

    Deux effets : le lecteur PDF affiche "102" la ou il affichait "98" (les
    numeros de page collent enfin a ceux imprimes sur le manuel), et le PDF
    devient autonome — 'extraire' et 'chapitres' y lisent le folio de depart au
    lieu de le deviner, ce qui marche aussi pour un PDF partiel.
    """
    import pikepdf

    with pikepdf.open(pdf, allow_overwriting_input=True) as doc:
        doc.Root.PageLabels = pikepdf.Dictionary(
            Nums=[0, pikepdf.Dictionary(S=pikepdf.Name.D, St=folio_initial)]
        )
        doc.docinfo["/FolioInitial"] = str(folio_initial)
        doc.save(pdf)


def lire_folio_initial(cfg, pdf):
    """Folio de la premiere page du PDF, lu dans ses metadonnees."""
    import pikepdf

    with pikepdf.open(pdf) as doc:
        valeur = doc.docinfo.get("/FolioInitial")
        if valeur is not None:
            return int(str(valeur))
    return folio_de_page(cfg, cfg["page_min"])


def commande_pdf(cfg, args):
    chemins = pages_disponibles(cfg)
    if not chemins:
        sys.exit(f"Aucune image dans {DOSSIER_PAGES}. Lancer 'download' d'abord.")
    sortie = Path(args.sortie) if args.sortie else DOSSIER_PDF / "manuel_complet.pdf"
    if not sortie.is_absolute():
        sortie = RACINE / sortie
    premier_folio = folio_de_page(cfg, page_de_nom(cfg, chemins[0]))
    fabriquer_pdf(chemins, sortie)

    if not args.purge:
        poser_folios(sortie, premier_folio)
        return 0

    print("\n  Vérification octet par octet avant suppression des originaux…")
    if not verifier_pdf(sortie, chemins):
        print("  Vérification ÉCHOUÉE : les JPG sont conservés.")
        return 1
    poids = sum(c.stat().st_size for c in chemins) / 1024 / 1024
    for c in chemins:
        c.unlink()
    print(f"  {len(chemins)} images vérifiées puis supprimées ({poids:.0f} Mo libérés).")
    poser_folios(sortie, premier_folio)
    print("  Les pages restent récupérables : commande 'extraire'.")
    return 0


def ardoise(texte):
    """Transforme un titre de chapitre en nom de fichier sans accent ni espace."""
    sans_accent = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", sans_accent.lower()).strip("_")[:60]


def pdf_source(args):
    """Le PDF global, source de verite une fois les JPG purges."""
    chemin = Path(args.depuis) if getattr(args, "depuis", None) else DOSSIER_PDF / "manuel_complet.pdf"
    if not chemin.is_absolute():
        chemin = RACINE / chemin
    if not chemin.exists():
        sys.exit(f"PDF introuvable : {chemin}. Lancer 'pdf' d'abord.")
    return chemin


def commande_chapitres(cfg, args):
    """Decoupe le PDF global en un PDF par chapitre, sans reencodage.

    On decoupe le PDF plutot que de repartir des JPG : les pages y sont deja et
    pikepdf recopie les flux images tels quels, donc le resultat est identique a
    l'original meme quand le dossier pages/ a ete purge.
    """
    import pikepdf

    chapitres = cfg.get("chapitres") or []
    if not chapitres:
        sys.exit("Aucun chapitre dans la configuration. Remplir la clé 'chapitres' "
                 "du JSON (num, titre, folio_debut, folio_fin).")
    source = pdf_source(args)
    DOSSIER_PDF.mkdir(exist_ok=True)
    premier_folio = lire_folio_initial(cfg, source)

    total = 0
    with pikepdf.open(source) as doc:
        for ch in chapitres:
            debut = ch["folio_debut"] - premier_folio
            fin = ch["folio_fin"] - premier_folio
            if debut < 0 or fin >= len(doc.pages):
                print(f"  ! {ch.get('slug', ch.get('titre'))} : folios hors du PDF, ignoré")
                continue
            extrait = pikepdf.new()
            for page in doc.pages[debut:fin + 1]:
                extrait.pages.append(page)
            # Un sous-dossier par theme, un fichier par slug ; a defaut de slug on
            # retombe sur le titre translittere, pour rester utilisable avec la
            # config d'un autre manuel.
            dossier = DOSSIER_PDF / ch["theme"] if ch.get("theme") else DOSSIER_PDF
            dossier.mkdir(parents=True, exist_ok=True)
            sortie = dossier / f"{ch.get('slug') or ardoise(ch['titre'])}.pdf"
            extrait.save(sortie)
            poser_folios(sortie, ch["folio_debut"])
            poids = sortie.stat().st_size / 1024 / 1024
            total += poids
            chemin = sortie.relative_to(DOSSIER_PDF)
            print(f"  {str(chemin):72s} folios {ch['folio_debut']:>3}-{ch['folio_fin']:<3} "
                  f"{fin - debut + 1:>3} p.  {poids:5.1f} Mo")
    print(f"\n  {len(chapitres)} sections, {total:.0f} Mo au total")
    return 0


def commande_signets(cfg, args):
    """Pose un signet par section dans le PDF global.

    Permet de sauter directement au bon chapitre depuis le panneau lateral du
    lecteur PDF, sans dupliquer la moindre page.
    """
    import pikepdf

    chapitres = cfg.get("chapitres") or []
    if not chapitres:
        sys.exit("Aucune section dans la configuration.")
    source = pdf_source(args)
    premier_folio = lire_folio_initial(cfg, source)

    with pikepdf.open(source, allow_overwriting_input=True) as doc:
        with doc.open_outline() as plan:
            plan.root.clear()
            themes = {}
            for ch in chapitres:
                index = ch["folio_debut"] - premier_folio
                if not 0 <= index < len(doc.pages):
                    continue
                entree = pikepdf.OutlineItem(ch["titre"], index)
                theme = ch.get("theme")
                if not theme:
                    plan.root.append(entree)
                    continue
                if theme not in themes:
                    # Le signet du theme pointe sur la premiere page de sa premiere
                    # section : cliquer "Espace et geometrie" ouvre le chapitre 13.
                    parent = pikepdf.OutlineItem(libelle_theme(cfg, theme), index)
                    plan.root.append(parent)
                    themes[theme] = parent
                themes[theme].children.append(entree)
        doc.save(source)
    print(f"  {len(chapitres)} signets posés dans {source.name}")
    return 0


def libelle_theme(cfg, theme):
    """Libelle lisible du theme, pris dans la config ; a defaut deduit du slug."""
    libelle = (cfg.get("themes") or {}).get(theme)
    if libelle:
        return libelle
    texte = re.sub(r"^\d+_", "", theme).replace("_", " ")
    return texte[:1].upper() + texte[1:]


def commande_extraire(cfg, args):
    """Ressort une page en JPG d'origine depuis le PDF (pour un Google Doc, etc.)."""
    import pikepdf

    source = pdf_source(args)
    premier_folio = lire_folio_initial(cfg, source)
    with pikepdf.open(source) as doc:
        for folio in args.folios:
            index = folio - premier_folio
            if not 0 <= index < len(doc.pages):
                print(f"  ! folio {folio} hors du PDF")
                continue
            image = list(doc.pages[index].images.values())[0]
            destination = Path(args.dossier) / f"folio-{folio}.jpg"
            destination.parent.mkdir(parents=True, exist_ok=True)
            # read_raw_bytes rend le flux JPEG tel qu'il est stocke : aucun
            # decodage, aucun reencodage, le fichier est celui d'origine.
            destination.write_bytes(image.read_raw_bytes())
            print(f"  {destination}  ({destination.stat().st_size / 1024:.0f} Ko)")
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
    p_pdf.add_argument("--purge", action="store_true",
                       help="supprimer les JPG une fois vérifiés dans le PDF")

    p_ch = sous.add_parser("chapitres", help="découper le PDF en un PDF par chapitre")
    p_ch.add_argument("--depuis", help="PDF source (défaut : pdf/manuel_complet.pdf)")

    p_si = sous.add_parser("signets", help="poser un signet par section dans le PDF global")
    p_si.add_argument("--depuis", help="PDF source (défaut : pdf/manuel_complet.pdf)")

    p_ex = sous.add_parser("extraire", help="ressortir une page en JPG depuis le PDF")
    p_ex.add_argument("folios", nargs="+", type=int, help="numéro(s) de folio")
    p_ex.add_argument("--depuis", help="PDF source (défaut : pdf/manuel_complet.pdf)")
    p_ex.add_argument("--dossier", default=".", help="dossier de destination")

    args = parseur.parse_args()
    cfg = charger_config(args.config)

    return {
        "download": commande_download,
        "pdf": commande_pdf,
        "chapitres": commande_chapitres,
        "signets": commande_signets,
        "extraire": commande_extraire,
    }[args.commande](cfg, args)


if __name__ == "__main__":
    sys.exit(main())
