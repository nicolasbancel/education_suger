---
name: edition_cours
description: Workflow d'édition assistée de cours de 6ème dans Google Docs avec respect strict du formatting, des conventions pédagogiques et logging des retours. Activer quand l'utilisateur veut travailler sur, modifier, compléter, ajouter du contenu à une section d'un chapitre, ou pointe vers un Google Doc de cours avec une section précise.
---

## Quand activer ce skill

Activer dès que l'utilisateur :
- demande de **travailler sur**, **modifier**, **compléter**, **rédiger**, **ajouter** du contenu à une section d'un chapitre (ex : "on bosse sur la section graphiques linéaires du chapitre 6", "ajoute un exemple sur les fractions équivalentes", "reformule l'intro du chap 8")
- demande de **créer un nouveau chapitre** ou un **squelette** de Doc (ex : "crée le chapitre 12 sur périmètres et aires", "fais-moi un squelette de Doc pour le chap N")
- pointe vers un **Google Doc** de cours avec un nom de section
- évoque une **correction** ou **enrichissement** de cours (pas d'interro — pour les interros voir `correction_interro` et `generation_calcul_mental`)

Ne PAS activer pour : génération d'interros, fiches d'exercices (séparé), corrections de DS/DM.

## Étape 1 — Charger la mémoire (OBLIGATOIRE au démarrage)

Avant toute proposition de contenu, lire dans l'ordre **tous** ces fichiers du repo :

1. `01_2526_6emes_maths/cours_edition/index.md` — résoudre nom du chapitre → URL Google Doc.
2. `00_conventions/google_docs.md` — hiérarchie de titres, polices (Montserrat 12/14/16), conventions tableaux, mise en exergue, notations.
3. `00_conventions/pedagogie/langage.md` — vocabulaire, registre, infinitif vs impératif.
4. `00_conventions/pedagogie/structure.md` — séquence pédagogique (inductif/déductif).
5. `00_conventions/pedagogie/exemples.md` — choix d'exemples, ancrage quotidien.
6. `00_conventions/pedagogie/erreurs_types.md` — **TRÈS IMPORTANT** : historique des erreurs déjà commises. RELIRE pour ne pas les refaire.

Annoncer à l'utilisateur en une phrase : "Mémoire chargée — conventions + erreurs_types. On peut démarrer."

## Étape 2a — Créer un nouveau Doc (si création)

Quand l'utilisateur demande la création d'un nouveau chapitre / squelette :

1. Demander (ou déduire) :
   - **Numéro et titre du chapitre** (ex : "Chapitre 12 - Périmètres et aires")
   - **Dossier Drive cible** (URL `https://drive.google.com/drive/u/0/folders/<id>`)
   - **Structure** : H2 (grandes parties) + H3 (sous-sections). Préférer la numérotation **manuelle** des H2 ("I. Périmètres", "II. Aires") dès le départ pour éviter le piège des listes auto cassées.

2. Construire un fichier markdown-like :
   ```
   # Chapitre N - <Titre>
   ## I. <Partie 1>
   ### <Sous-section>
   ### <Sous-section>
   ## II. <Partie 2>
   ### <Sous-section>
   ```

3. Lancer la création :
   ```
   cd /Users/nicolasbancel/.claude/scripts
   .venv/bin/python gdoc_create.py \
       --folder "<URL_dossier_drive>" \
       --title "Chapitre N - <Titre>" \
       --structure /tmp/struct_chapN.md \
       --account perso
   ```

4. Le script applique automatiquement Montserrat (12 / 14 / 16 / 18 pt selon le niveau de heading).

5. **Mettre à jour `01_2526_6emes_maths/cours_edition/index.md`** avec une nouvelle ligne pour ce chapitre (URL retournée par le script + statut `squelette`).

Ensuite : continuer en Étape 3 si on enchaîne sur du contenu, ou conclure en Étape 5.

## Étape 2 — Cibler la section (si édition)

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
- Le formatting (`00_conventions/google_docs.md`)
- Les conventions pédagogiques (`00_conventions/pedagogie/*.md`)
- Le registre 6ème (vocabulaire concret, exemples ancrés dans le quotidien)

Itérer jusqu'à validation explicite ("OK", "push", "vas-y").

## Étape 3 bis — Prendre du recul et challenger (OBLIGATOIRE avant le push)

Avant de pousser le contenu validé en Étape 3, **toujours s'arrêter pour challenger** ce qui va être poussé. Ne pas se contenter de "le user a dit OK".

Demander explicitement à l'utilisateur (en une réponse texte structurée) :

> "Avant de pousser, je prends du recul. Voici ce que je remarque qui pourrait manquer ou être enrichi :
> - **[Lacune potentielle 1]** : [ce qui pourrait manquer + pourquoi]
> - **[Lacune potentielle 2]** : [exemple alternatif intéressant à ajouter]
> - **[Lien inter-chapitres]** : [un rappel utile vers un autre chap qu'on pourrait insérer]
> - **[Différenciation]** : [un exemple plus difficile pour les élèves à l'aise / plus simple pour ceux en difficulté]
> 
> Tu veux qu'on intègre quelque chose de ça avant de pousser, ou on push tel quel ?"

Domaines à passer en revue à chaque fois :
1. **Définitions manquantes** : y a-t-il une notion utilisée sans être définie ?
2. **Exemples gradués** : a-t-on un exemple simple + un exemple difficile, ou que du standard ?
3. **Liens inter-chapitres** : un rappel utile vers un chap antérieur (ex : conversions ↔ chap 4 fractions) ?
4. **Pièges classiques** : y a-t-il une erreur fréquente d'élève qui mériterait un encadré "⚠ Attention" ?
5. **Différenciation** : contenu équivalent pour les élèves à l'aise vs ceux en difficulté ?
6. **Cohérence pédagogique** : la séquence respecte-t-elle le style du chapitre (inductif / déductif) défini dans `pedagogie/structure.md` ?
7. **"À retenir"** : est-ce qu'un encadré de synthèse serait pertinent en fin de section ?

Cette étape est un **garde-fou contre le push prématuré** : Claude propose du contenu qui satisfait la demande littérale mais qui peut rater des dimensions pédagogiques que l'utilisateur juge importantes. Mieux vaut poser 30 secondes de questions avant qu'un push à refaire.

Si l'utilisateur dit "push tel quel" : on push. Sinon, on retourne à l'Étape 3 pour intégrer.

## Étape 4 — Push

### ⚠️ Règle d'or : préférer les opérations chirurgicales

Par défaut, **NE PAS écraser une section déjà rédigée avec `write-section`** — ça détruit toute modification manuelle que l'utilisateur a faite dans le Doc entre 2 sessions. `write-section` est réservé à :
- La **1ère rédaction** d'une section vide (squelette)
- Les cas où l'utilisateur dit explicitement "réécris toute cette section"

Pour toute autre modification, choisir l'outil chirurgical adapté :

| Action | Outil |
|---|---|
| Corriger une phrase ("X" → "Y") | `replaceAllText` (script ad-hoc Python) |
| Ajouter un paragraphe à un endroit précis | `insertText` à un index ancré sur du texte existant |
| Ajouter un encadré / un tableau | `gdoc_insert_box.py` / `gdoc_insert_table.py` (déjà non-destructifs) |
| Re-appliquer les conventions visuelles sans toucher au texte | `gdoc_apply_styles.py` |
| Modifier le style d'un range précis | `updateTextStyle` / `updateParagraphStyle` ciblé (script ad-hoc) |

Avant tout `write-section` itératif, **demander à l'utilisateur** : *"Tu as fait des modifications manuelles dans le Doc depuis le dernier push ?"*. Si oui : basculer obligatoirement sur opérations chirurgicales.



### Texte (paragraphes + bullets natifs)
```
.venv/bin/python gdoc.py --account perso write-section "<URL>" "<Section>" \
    --line-spacing {100,150} \
    --stdin < /tmp/contenu.txt
```
Le script applique automatiquement Montserrat 12pt, nettoie les bullets hérités, et **alerte** si la numérotation auto des H2 voisins est cassée. Lire le retour — s'il contient `⚠️`, signaler à l'utilisateur **avant de continuer**.

**Choix du `--line-spacing`** (voir `00_conventions/google_docs.md` section "Interligne") :
- `--line-spacing 100` (défaut) : texte sans trous (intro, définition complète, etc.)
- `--line-spacing 150` : texte avec trous à remplir par l'élève (cours à trous, exercices) — laisse de la place pour écrire

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

### Encadré stylé (À retenir / Définition / Méthode / Rappel / Attention)
```
.venv/bin/python gdoc_insert_box.py "<URL>" \
    --section "<Section>" \
    --after-text "<phrase d'ancrage>" \
    --type {a-retenir,definition,methode,rappel,attention} \
    --content "<texte du corps>" \
    --account perso
```
Voir `00_conventions/google_docs.md` section "Encadrés" pour le détail des 5 types (couleurs, usages). Le script applique automatiquement le label, les couleurs de fond/bordure et la typo. Ne PAS écrire le label ("À RETENIR", "Définition", etc.) dans `--content` — il est ajouté automatiquement.

Usage type :
- `--type a-retenir` à la fin d'une grande section pour synthétiser les formules/règles clés.
- `--type definition` pour une notion à mémoriser (périmètre, π, formule nommée).
- `--type methode` pour une procédure pas-à-pas (conversion, calcul).
- `--type rappel` pour pointer un chapitre antérieur ("rappel du chap 4…").
- `--type attention` pour un piège classique (ex : conversions d'aires à 2 rangs vs 1).

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
- `00_conventions/pedagogie/langage.md` — vocabulaire, registre, tournures
- `00_conventions/pedagogie/structure.md` — séquence des blocs (Déf → Méthode → Exemple)
- `00_conventions/pedagogie/exemples.md` — types et progression des exemples
- `00_conventions/pedagogie/erreurs_types.md` — incidents techniques ou pédagogiques à ne pas refaire

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
