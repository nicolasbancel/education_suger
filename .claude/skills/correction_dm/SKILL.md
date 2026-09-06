---
name: correction_dm
description: Use when l'utilisateur veut piloter, analyser ou corriger un DM "numérique" où chaque élève a sa propre Google Sheet (saisie, formules, graphiques) — par ex. dossiers contenant un google_sheets_links.md et un énoncé .tex. Couvre 3 niveaux : tableau de bord d'avancement de la cohorte (qui a commencé, erreurs communes), correction + notation individuelle avec fiches .tex, et (V2) commentaires ancrés sur les sheets. L'agent lit l'énoncé, fige une grille de lecture, puis applique des outils déterministes.
---

# correction_dm : corriger des DM numériques sur Google Sheets

Agent d'aide à la correction de devoirs où chaque élève travaille sur SA copie d'une
Google Sheet. Conçu pour être **réutilisable d'un DM à l'autre** : seul change un
fichier `grille.yaml` que l'agent déduit de l'énoncé.

## Règle d'or (non négociable)

> **L'agent décide _quoi_ vérifier (en lisant l'énoncé). Les outils déterministes _font_ la vérification.**

Ne jamais juger « à l'œil » si une cellule contient une formule, si un graphique
existe, etc. Toujours passer par les scripts Python ci-dessous. C'est ce qui rend
la correction reproductible, applicable à 25+ élèves et gratuite à relancer.

## Architecture en 3 niveaux

| Niveau | But | Écrit sur les sheets ? | État |
|---|---|---|---|
| **0** | Tableau de bord cohorte : qui a commencé, avancement, erreurs communes | Non | ✅ collecteur prêt |
| **1** | Correction + notation individuelle → fiche `.tex`/PDF par élève | Non (brouillon prof) | ✅ |
| **2** | Feedback dans la sheet : **note** (ancrée, silencieuse) ou **commentaire + @mention** (non épinglé à la cellule, mais ping ~10 min) | Oui (après validation) | ✅ |
| **Ping** | Notifier l'élève → **commentaire @mention** (~10 min, reste dans la sheet) ou **email Gmail** (instantané) | Oui (après validation) | ✅ |

## Outils (dans `~/.claude/scripts/`, venv `.venv/bin/python`)

- `gsheet.py` — `read_formulas` (formule vs valeur en dur via `valueRenderOption=FORMULA`),
  `get_charts` (type + plages source des graphiques). CLI : `formulas`, `charts`, `tabs`, `read`.
- `gdrive_revisions.py activity <id> --student-email <email>` — signaux de démarrage :
  `date_creation`, `createur` + `cree_par_eleve` (gère « parfois l'élève crée la sheet »),
  `premier_edit_eleve` / `dernier_edit_eleve` (UTC + heure de Paris), `revisions_eleve`
  (timeline des moments de travail), `sessions_eleve` (séances estimées). Passer l'email isole
  les éditions de l'élève de celles du prof.
  - **Fiable** : QUAND l'élève a travaillé, combien de moments distincts → régulier vs dernière minute.
  - **Pas fiable** : la DURÉE de chaque séance (`duree_min_estimee` ≈ 0) — Google élague les
    éditions rapprochées (1 révision retenue par moment). Pour des durées réelles → Drive Activity
    API (scope + activation GCP en plus), à faire dans une feature dédiée « durées ».
- `correction_dm_collect.py` — **collecteur grille-driven** : applique `grille.yaml` aux sheets
  → un `faits.json` par élève (cellule : valeur+formule+type+OK ; données ; graphiques ;
  démarrage ; score déterministe). [Étape B.1]
- `correction_dm_dashboard.py` — **Niveau 0** : agrège `faits/*.json` → markdown et/ou Google
  Sheet de reporting (`--out`, `--report-sheet`, `--create-report-sheet`+`--folder`, `--run-date`).
  Le reporting Sheet est **color-codé** (vert=Correct, jaune=Incorrect, rouge=Not started),
  applique les **conventions du prof** (en-tête bleu `#c9daf8`, Arial 10, bordures, via
  `gsheet.cmd_format`), et crée un **onglet de détail daté par jour de run**
  (`Détail élèves JJ/MM`). [Étape B.2]
- `correction_dm_fiche.py` — **Niveau 1** : `faits.json` + `draft.json` (commentaire/qualitatif)
  → fiche `correction.tex` + PDF, via le template `fiche_correction.tex`. [Étape C]
- `correction_dm_comments.py` — **Niveau 2 (in-cell)** : `build` (faits → `comments.json` proposés,
  aucune écriture) puis `publish --confirm` (écrit des NOTES ancrées sur la sheet élève). [Étape D]
- `correction_dm_email.py` — **Ping élève** : `build` (links+grille → `emails.json`, n'envoie rien)
  puis `send --confirm` (envoie via Gmail). Seul canal qui notifie réellement l'élève. [Étape E]

Compte Google : **`perso`** pour ce repo (propriétaire des sheets élèves). Surchargé par
`compte:` dans la grille ou `--account`.

## Organisation des fichiers

```
<dossier_du_DM>/
  <enonce>.tex
  google_sheets_links.md          # liens élèves (gitignoré — PII)
  correction/
    grille.yaml                    # produite par l'agent, validée par le prof (PAS de PII → versionnable)
    faits/<prenom>_<nom>.json      # sortie collecteur (gitignoré — PII)
    _tableau_de_bord.md            # Niveau 0 (gitignoré — PII)
    corrections/<eleve>/           # Niveau 1 (gitignoré — PII)
```

Les patterns `**/correction/faits/`, `**/correction/corrections/`,
`**/correction/_tableau_de_bord.md` sont déjà dans le `.gitignore` du repo.

## Procédure

### Étape A — Produire la grille (une fois par DM)

1. Lire l'énoncé `.tex`. En déduire, par onglet : les **cellules attendues** (référence,
   type `formule`/`valeur_en_dur`, fonctions acceptées **FR ET EN**), les **plages de
   saisie**, les **graphiques attendus** (type + colonnes), et les **blocs qualitatifs**
   (réponses rédigées — non mesurables automatiquement). Affecter des points.
2. Écrire `correction/grille.yaml` (voir le format dans `grille.yaml` d'un DM existant,
   ex. `dm_gestion_donnees/correction/grille.yaml`).
3. **Demander au prof de valider/corriger la grille** (~30 s). Une fois validée, elle est figée.

Tolérances de fonctions à prévoir : MOYENNE/AVERAGE, COUNTIF/NB.SI, COUNTA/NBVAL, SOMME/SUM, MAX, MIN.

### Étape B — Niveau 0 : tableau de bord d'avancement

**B.1 — Collecter** les faits déterministes (rejouable autant qu'on veut pendant le DM) :

```bash
~/.claude/scripts/.venv/bin/python ~/.claude/scripts/correction_dm_collect.py \
  --grille <DM>/correction/grille.yaml \
  --students <DM>/google_sheets_links.md \
  --out <DM>/correction/faits
```

**B.2 — Agréger** en tableau de bord avec `correction_dm_dashboard.py` : vue d'ensemble
(taux de démarrage, score moyen, liste des « pas commencé » à relancer), **erreurs les plus
communes** par item (ex. « G9 MAX : 16/17 KO » ; types formule/dur/vide → adapter l'énoncé),
détail par élève (✓/✗ par item), démarrage/régularité (1er edit, séances).

**Deux sorties — TOUJOURS DEMANDER AU PROF laquelle (ou les deux) :**

1. **Fichier markdown en dur** (`--out <DM>/correction/_tableau_de_bord.md`).
2. **Google Sheet de reporting.** Demander au prof :
   - soit **il fournit l'URL** d'une sheet existante → `--report-sheet <url>` (on n'écrit/efface
     que l'onglet `Synthèse` et l'onglet `Détail élèves JJ/MM` du jour, jamais le reste de SA sheet) ;
   - soit **on la crée** → `--create-report-sheet "<titre>"`, et **demander un `--folder <url>`
     optionnel** (id/URL d'un dossier Drive cible ; sans folder → racine du Drive).

   **Conventions de remplissage (appliquées automatiquement, défaut) :**
   - **Onglet de détail daté par jour de run** : `Détail élèves JJ/MM` (ex. `Détail élèves 07/06`).
     Un run le lendemain crée `Détail élèves 08/06` → **historique d'avancement conservé**.
     L'onglet `Synthèse` reste unique et rafraîchi à chaque run. `--run-date JJ/MM` force la date
     (défaut : aujourd'hui, fuseau Europe/Paris).
   - **Cases de détail = mots + couleur** (pas de "OK"/"KO") : chaque case d'item contient
     littéralement `Correct` (fond vert `#b6d7a8`), `Incorrect` (fond jaune `#ffe599`) ou
     `Not started` (fond rouge `#ea9999`). États : `Correct` = `ok` ; `Incorrect` = tenté
     mais faux ; `Not started` = non tenté / cellule vide (`type == "vide"`, `rempli == 0`,
     ou pas de graphique). Pas de légende séparée (le mot est dans la case).
   - **Colonne « Lien »** (2ᵉ colonne) : lien cliquable « Ouvrir la copie » vers la Google
     Sheet de chaque élève (URL construite depuis `sheet_id` des faits), pour aller relire
     la copie en un clic.
   - **Conventions Google Sheet** (cf. `one_off_projects/conventions/google_sheets_formatting.md`) :
     en-tête bleu `#c9daf8` gras, Arial 10, bordures — via `gsheet.cmd_format`.

```bash
# Exemple création dans un dossier précis :
~/.claude/scripts/.venv/bin/python ~/.claude/scripts/correction_dm_dashboard.py \
  --grille <DM>/correction/grille.yaml --faits <DM>/correction/faits \
  --create-report-sheet "[Reporting] <nom du DM>" --folder "<url_dossier_drive>"
# Ou refresh d'une sheet existante : --report-sheet "<url>"
# Ou markdown seul : --out <DM>/correction/_tableau_de_bord.md
```

Re-jouable autant de fois qu'on veut pendant que le DM est en cours.

### Étape C — Niveau 1 : correction + notation individuelle

Hybride : le **tableau de barème** (item par item, OK/KO + points) vient des `faits.json`
(déterministe, aucune note inventée) ; le **commentaire** et les **points qualitatifs**
(observations rédigées sur copie double) viennent d'un **draft JSON rédigé par l'agent**.

**C.1 — L'agent rédige un draft par élève.** Lire `faits/<eleve>.json` (ce que l'élève a
fait/manqué + signaux de démarrage) et, si le prof a transcrit les observations papier, les
intégrer. Produire un JSON :

```json
{
  "commentaire": "Texte LaTeX (peut contenir \\textbf{...}, \\texttt{...}). Personnalisé, bienveillant, factuel : ce qui est réussi, ce qui manque (citer les cellules), un conseil.",
  "qualitatif": { "obs_calcul_mental": 3, "obs_giec": 1 }
}
```

`qualitatif` = points des blocs `qualitatif` de la grille (depuis la copie double). Un bloc
non noté → ligne « à noter » dans la fiche (0 compté), à compléter à la main.

**C.2 — Générer la fiche** (remplit le template `fiche_correction.tex` + compile le PDF) :

```bash
~/.claude/scripts/.venv/bin/python ~/.claude/scripts/correction_dm_fiche.py \
  --faits <DM>/correction/faits/<eleve>.json \
  --grille <DM>/correction/grille.yaml \
  --template <DM>/correction/fiche_correction.tex \
  --draft <draft.json> \
  --out-dir <DM>/correction/corrections
# → <DM>/correction/corrections/<eleve>/correction.pdf
```

Le template `fiche_correction.tex` (style du prof : en-tête Suger, table à en-tête lavande,
colonne « Obtenus » color-codée vert/jaune/rouge, boîte commentaire bleue, encart vert
« Comment tu as travaillé ») est **versionnable** (pas de PII). Rien n'est publié sur les
sheets : la fiche est un brouillon validé par le prof avant d'être rendue.

### Étape D — Niveau 2 : notes ancrées sur les cellules

**CONSTAT empirique (testé)** :
- Un *commentaire* Drive créé via l'API NE s'ancre PAS à une cellule choisie : l'ancre est un
  **entier opaque serveur** (`{"type":"workbook-range","uid":0,"range":"2010871162"}`), non
  calculable depuis la cellule. On peut seulement RÉUTILISER l'ancre d'un commentaire déjà
  présent sur cette cellule, pas en fabriquer une pour une cellule vide.
- En revanche, un **@mention dans un commentaire NOTIFIE bien l'élève** (email "X vous a
  mentionné", regroupé par Google, délai ~10 min). [corrige une conclusion trop rapide : la
  notif n'était simplement pas encore arrivée lors du 1er test.]
- Les **notes** (triangle en coin) s'ancrent à la cellule mais ne notifient pas.

Donc deux options in-sheet : **note** (ancrée, silencieuse) ou **commentaire + @mention**
(non épinglé à une cellule précise, mais qui PING l'élève sous ~10 min ; le texte indique quelle
cellule regarder). Et l'**email** (Étape E) reste l'option de notification instantanée.

Two-pass (écriture visible par l'élève, difficilement réversible) :

```bash
# 1. PROPOSER (n'écrit rien) : génère un comments.json à partir des KO des faits
~/.claude/scripts/.venv/bin/python ~/.claude/scripts/correction_dm_comments.py build \
  --faits <DM>/correction/faits/<eleve>.json \
  --out  <DM>/correction/corrections/<eleve>/comments.json
#    → le prof RELIT / édite ce fichier (texte, cellules)

# 2. PUBLIER (écrit sur la sheet de l'élève) — APRÈS validation, exige --confirm
#    a) NOTE ancrée, silencieuse (défaut) :
~/.claude/scripts/.venv/bin/python ~/.claude/scripts/correction_dm_comments.py publish \
  --comments <DM>/correction/corrections/<eleve>/comments.json \
  --sheet "<url_sheet_eleve>" --confirm
#    b) COMMENTAIRE + ping de l'élève (~10 min), feedback dans la sheet :
~/.claude/scripts/.venv/bin/python ~/.claude/scripts/correction_dm_comments.py publish \
  --comments <DM>/correction/corrections/<eleve>/comments.json \
  --sheet "<url_sheet_eleve>" --mode comment --mention <email_élève> --confirm
#    sans --confirm = dry-run (affiche le texte exact, mention comprise)
```

L'agent peut aussi fournir des remarques sur-mesure via le draft
(`commentaires_cellules: [{tab, cell, text}]`), qui remplacent la proposition auto.
En `--mode comment`, le script ajoute **tout seul** le `@<email>` (passé via `--mention`) en
tête du commentaire (ping ~10 min) et situe la cellule dans le texte (le commentaire n'est pas
épinglé à la cellule, limite API). En `--mode note`, le texte est posé tel quel sur la cellule.

### Étape E — Ping élève par email (notification instantanée)

Les notes ne notifient pas ; un commentaire @mention notifie sous ~10 min (Étape D). Pour une
notification **instantanée** et un message riche → email via Gmail (compte `perso`, scope
`gmail.send`). Two-pass :

```bash
# 1. PRÉPARER (n'envoie rien) : un email par élève (objet + corps), depuis les liens + la grille
~/.claude/scripts/.venv/bin/python ~/.claude/scripts/correction_dm_email.py build \
  --students <DM>/google_sheets_links.md --grille <DM>/correction/grille.yaml \
  --faits <DM>/correction/faits --with-score \
  --out <DM>/correction/emails.json
#    → le prof RELIT / édite emails.json (corps, objet)

# 2. ENVOYER — exige --confirm ; --only <adresse> ou --limit N pour tester d'abord
~/.claude/scripts/.venv/bin/python ~/.claude/scripts/correction_dm_email.py send \
  --emails <DM>/correction/emails.json --confirm
#    sans --confirm = dry-run (liste les destinataires)
```

Toujours tester avec `--only <ta_propre_adresse>` avant un envoi groupé. `emails.json`
contient des adresses élèves (PII) → gitignoré.

## Garde-fous

- **RGPD** : ne jamais committer `faits/`, `corrections/`, `_tableau_de_bord.md`,
  `emails.json`, `google_sheets_links.md`. Vérifier le `.gitignore` avant tout `git add`.
- **Publication** : toute écriture sur une sheet élève (notes) ou tout email est visible/reçu par
  l'élève et difficilement réversible → toujours `build` → relecture prof → `publish/send --confirm`,
  et tester l'email avec `--only <ta_propre_adresse>` avant l'envoi groupé.
- **Scope Gmail** : l'envoi requiert `gmail.send` sur le compte `perso` (déjà ajouté à
  `auth_google.py`). Si une autre feature requiert d'activer une API/scope → le DEMANDER au prof.
