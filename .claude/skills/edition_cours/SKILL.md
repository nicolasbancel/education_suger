---
name: edition_cours
description: Workflow d'édition assistée de cours de 6ème dans Google Docs avec respect strict du formatting, des conventions pédagogiques et logging des retours. Activer quand l'utilisateur veut travailler sur, modifier, compléter, ajouter du contenu à une section d'un chapitre, ou pointe vers un Google Doc de cours avec une section précise.
---

## Quand activer ce skill

Activer dès que l'utilisateur :
- demande de **travailler sur**, **modifier**, **compléter**, **rédiger**, **ajouter** du contenu à une section d'un chapitre (ex : "on bosse sur la section graphiques linéaires du chapitre 6", "ajoute un exemple sur les fractions équivalentes", "reformule l'intro du chap 8")
- pointe vers un **Google Doc** de cours avec un nom de section
- évoque une **correction** ou **enrichissement** de cours (pas d'interro — pour les interros voir `correction_interro` et `generation_calcul_mental`)

Ne PAS activer pour : génération d'interros, fiches d'exercices (séparé), corrections de DS/DM.

## Étape 1 — Charger la mémoire (OBLIGATOIRE au démarrage)

Avant toute proposition de contenu, lire dans l'ordre **tous** ces fichiers du repo :

1. `01_2526_6emes_maths/cours_edition/index.md` — résoudre nom du chapitre → URL Google Doc.
2. `01_2526_6emes_maths/cours_edition/formatting_guide.md` — hiérarchie de titres, polices (Montserrat 12/14/16), conventions tableaux, mise en exergue, notations.
3. `01_2526_6emes_maths/cours_edition/pedagogie/langage.md` — vocabulaire, registre, infinitif vs impératif.
4. `01_2526_6emes_maths/cours_edition/pedagogie/structure.md` — séquence pédagogique (inductif/déductif).
5. `01_2526_6emes_maths/cours_edition/pedagogie/exemples.md` — choix d'exemples, ancrage quotidien.
6. `01_2526_6emes_maths/cours_edition/pedagogie/erreurs_types.md` — **TRÈS IMPORTANT** : historique des erreurs déjà commises. RELIRE pour ne pas les refaire.

Annoncer à l'utilisateur en une phrase : "Mémoire chargée — conventions + erreurs_types. On peut démarrer."

## Étape 2 — Cibler la section

Si l'utilisateur a donné un nom de chapitre, résoudre l'URL via `index.md`. Sinon, demander l'URL directement.

Lister les sections du Doc pour confirmer le titre exact :
```
cd /Users/nicolasbancel/.claude/scripts
.venv/bin/python gdoc.py --account perso sections "<URL>"
```

Lire le contenu actuel de la section ciblée :
```
.venv/bin/python gdoc.py --account perso read-section "<URL>" "<Titre exact>"
```

⚠️ Limite connue : `read-section` ne retourne pas les images ni les tables existantes (seulement le texte des paragraphes).

## Étape 3 — Proposer du contenu, itérer

Discuter avec l'utilisateur. Toutes les propositions doivent **respecter en simultané** :
- Le formatting (`formatting_guide.md`)
- Les conventions pédagogiques (`pedagogie/*.md`)
- Le registre 6ème (vocabulaire concret, exemples ancrés dans le quotidien)

Itérer jusqu'à validation explicite ("OK", "push", "vas-y").

## Étape 4 — Push

### Texte (paragraphes + bullets natifs)
```
.venv/bin/python gdoc.py --account perso write-section "<URL>" "<Section>" --stdin < /tmp/contenu.txt
```
Le script applique automatiquement Montserrat 12pt, nettoie les bullets hérités, et **alerte** si la numérotation auto des H2 voisins est cassée. Lire le retour — s'il contient `⚠️`, signaler à l'utilisateur **avant de continuer**.

Format du contenu :
- Texte normal : paragraphes séparés par lignes vides
- Bullet natif Docs : ligne commençant par `- ` (un seul tiret + espace)
- Pas de tabulations `\t`, pas de tableau pipes `|` (voir ci-dessous)

### Tableau Docs natif
```
.venv/bin/python gdoc_insert_table.py "<URL>" \
    --section "<Section>" \
    --after-text "<phrase d'ancrage>" \
    --csv /tmp/data.csv \
    --account perso
```
CSV : 1ère ligne = en-têtes. Le script applique la convention complète (header gras + fond `#c9daf8`, données centrées H+V, Montserrat 10pt, padding 0,1 cm).

**JAMAIS** rédiger un tableau en pipes `|` dans le texte poussé via `write-section`.

### Image (PNG/JPG)
```
.venv/bin/python gdoc_insert_image.py "<URL>" "<Section>" "<chemin_local>" --account perso
```
Insertion en fin de section. ⚠️ L'image est **rendue publique sur Drive** (anyone with link) — requis par l'API. À signaler si le contenu pourrait être sensible.

### Remplacement ciblé (sans toucher au reste de la section)
Quand l'utilisateur veut juste reformuler quelques phrases sans refaire toute la section, utiliser `replaceAllText` via un script Python ad-hoc :
```python
docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
    {"replaceAllText": {
        "containsText": {"text": "ancien texte exact", "matchCase": True},
        "replaceText": "nouveau texte",
    }}
]}).execute()
```

## Étape 5 — Capitalisation (OBLIGATOIRE en fin de session)

Avant de conclure, demander explicitement :

> "On a fini ce bloc. Y a-t-il un retour, une correction ou une règle que tu veux que je logge dans `pedagogie/` pour ne pas refaire l'erreur ?"

Si oui : identifier le fichier cible et ajouter une entrée datée (format `YYYY-MM-DD — Titre court`) :
- `pedagogie/langage.md` — vocabulaire, registre, tournures
- `pedagogie/structure.md` — séquence des blocs (Déf → Méthode → Exemple)
- `pedagogie/exemples.md` — types et progression des exemples
- `pedagogie/erreurs_types.md` — incidents techniques ou pédagogiques à ne pas refaire

Suivre le template existant du fichier ciblé.

Si rien à logger : conclure proprement (résumé court de ce qui a été fait).

## Conventions transversales

- **Compte Google** : toujours `--account perso` pour les Docs de cours.
- **Langue** : français dans tout contenu poussé.
- **Guillemets** : droits `"..."` dans les fichiers `.md` du repo (jamais `«...»` ni typographiques).
- **En-tête de section markdown** : commencer à `##` (le `#` est réservé au titre du doc).
- **Erreurs API** : ne PAS retenter en boucle. Diagnostiquer (compte ? section existe ? scopes ?) et remonter à l'utilisateur.

## Pièges connus (voir `erreurs_types.md` pour le détail)

- `write-section` peut casser la numérotation auto des H2 voisins → le script alerte maintenant, lire son retour.
- Tableaux en pipes `|` = laid → toujours `gdoc_insert_table.py`.
- Consignes d'exercice à l'impératif → toujours **infinitif** dans les listes après "À toi de jouer".
