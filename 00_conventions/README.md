# Conventions

Point d'entrée unique pour toutes les conventions de rédaction, de formatage et de
pédagogie du repo. **Toute règle transverse vit ici**, quelle que soit la classe ou la
matière concernée.

Ce dossier est référencé dans le `CLAUDE.md` à la racine : il est donc chargé
automatiquement au démarrage de chaque session.

## Carte complète : où vit chaque fichier

Tout ce qui porte une convention ou un style dans ce repo, en un seul tableau. Les
règles **écrites** sont ici, dans `00_conventions/`. Le style LaTeX **implémenté** est à
la racine du repo, dans trois fichiers `.sty` (voir plus bas pourquoi).

| Fichier | Emplacement | S'applique à | Contenu |
|---|---|---|---|
| `README.md` | **ici** | — | ce fichier : l'index et le point de départ |
| `latex.md` | **ici** | LaTeX | balises, listes, figures, écriture des équations, décomposition des calculs |
| `workflow_latex.md` | **ici** | LaTeX | **procédure de travail** : compiler, vérifier le log, ouvrir le PDF à la page modifiée |
| `blocs_de_cours.md` | **ici** | les deux | **grammaire visuelle** : les six blocs d'un cours, lequel utiliser quand, comment chacun se signale, et **pourquoi** |
| `pieges_techniques.md` | **ici** | LaTeX, shell, scripts | les erreurs d'outillage qui échouent **silencieusement**, avec leur parade |
| `google_docs.md` | **ici** | Google Docs | hiérarchie de titres, polices, couleurs, tableaux, encadrés, indentation |
| `redaction_maths.md` | **ici** | les deux | structure d'un raisonnement rédigé : "On sait que / Or / Donc" |
| `redaction_physique.md` | **ici** | les deux | formules, conversions, application numérique, conclusion |
| `template_latex.tex` | **ici** | LaTeX | squelette de départ d'un document (classe, en-tête, packages) |
| `pedagogie/langage.md` | **ici** | les deux | vocabulaire, registre, vouvoiement, infinitif dans les consignes |
| `pedagogie/structure.md` | **ici** | les deux | séquence des blocs (inductif / déductif), intro motivante, rappels |
| `pedagogie/exemples.md` | **ici** | les deux | choix et progression des exemples, ancrage dans le quotidien |
| `pedagogie/erreurs_types.md` | **ici** | les deux | **historique daté des erreurs déjà commises. À relire avant de rédiger.** |
| `mypackages.sty` | racine du repo | LaTeX | les packages LaTeX chargés |
| `macros.sty` | racine du repo | LaTeX | raccourcis : `\dsheader`, `\fig`, `\trou`, `\ans` |
| `stylecours.sty` | racine du repo | LaTeX | style des cours : les 5 encadrés, tableaux d'exercices, palette, schémas |
| `gdoc*.py` | `~/.claude/scripts/` | Google Docs | application du style aux Docs (**hors repo**) |
| `cours_edition/index.md` | `01_2526_6emes_maths/` | Google Docs | table des URL des Docs de cours de 6ème |

La même carte figure dans le `CLAUDE.md` à la racine, qui est chargé automatiquement au
démarrage de chaque session.

## Deux formats de sortie, deux jeux de conventions

Les documents produits dans ce repo sortent sous deux formes, qui n'ont **rien en
commun techniquement**. Avant d'ouvrir un fichier de conventions, savoir dans lequel
des deux mondes on se trouve :

| | **LaTeX** | **Google Docs** |
|---|---|---|
| Ce que c'est | des fichiers `.tex` compilés en PDF par `pdflatex` | des documents en ligne, modifiés via l'API Google |
| Ce qu'on y fait | interros, DS, DM, corrections, fiches d'exercices, documents de calcul mental | les cours (Chapitre 0, Chapitre 12...) |
| Conventions de format | [`latex.md`](latex.md) | [`google_docs.md`](google_docs.md) |
| Style visuel | `stylecours.sty` (voir plus bas) | les scripts `gdoc_*.py` dans `~/.claude/scripts/` |
| Conventions de pédagogie | [`pedagogie/`](pedagogie/) : **communes aux deux** | idem |

Autrement dit : `latex.md` et `stylecours.sty` n'ont **aucun effet** sur un Google Doc,
et `google_docs.md` n'a **aucun effet** sur un PDF LaTeX. Les fichiers de `pedagogie/`,
eux, s'appliquent partout, parce qu'ils parlent de ce qu'on écrit, pas de comment c'est
mis en page.

## Style visuel des documents LaTeX : les trois `.sty` de la racine

Les encadrés, tableaux d'exercices et schémas ne sont pas décrits en prose ici : ils sont
**implémentés** en LaTeX, dans trois fichiers `.sty` situés **à la racine du repo**.

Un fichier `.sty` (pour "style") n'est pas un programme qu'on lance : c'est un bloc de
définitions qu'un document LaTeX charge au début, avant d'écrire quoi que ce soit. Ces
trois-là ne concernent **que le LaTeX**, jamais les Google Docs.

| Fichier | Rôle |
|---|---|
| [`../mypackages.sty`](../mypackages.sty) | la liste des packages LaTeX chargés (maths, tableaux, couleurs, TikZ...) |
| [`../macros.sty`](../macros.sty) | les raccourcis d'écriture : `\dsheader` (l'en-tête Collège Suger), `\fig` (une figure centrée), `\trou`, `\ans`... |
| [`../stylecours.sty`](../stylecours.sty) | le style des documents de cours : les 5 encadrés, les tableaux d'exercices, la palette, les schémas |

Chargement, dans cet ordre obligatoire (l'exemple suppose un document situé à deux
niveaux sous la racine, d'où les `../../`) :

```latex
\documentclass[11pt]{exam}
\usepackage{../../mypackages}
\usepackage{../../macros}
\usepackage{../../stylecours}
```

### Pourquoi ces trois fichiers sont à la racine et pas dans ce dossier

Parce qu'un `\usepackage` LaTeX désigne un chemin **relatif au document qui l'écrit**.
Or **156 fichiers `.tex`** du repo chargent déjà `mypackages` et `macros`, depuis cinq
profondeurs différentes (`mypackages`, `../mypackages`, `../../mypackages`,
`../../../mypackages`, `../../../../mypackages`). Les déplacer obligerait à corriger ces
156 fichiers, chacun selon sa profondeur. `stylecours.sty` a donc été placé **à côté
d'eux**, pour que les trois soient au même endroit.

### Ce qu'on modifie dans `stylecours.sty`

| Bloc | Ce qu'il règle |
|---|---|
| Palette | les 13 couleurs : fond et bordure de chaque encadré, barres d'exemple et d'exercice, en-têtes de tableau |
| Encadrés | `theorie`, `astuce`, `attention`, `aretenir`, `exemple` : épaisseur du trait, arrondi, marges, titre |
| Exercices | `exos`, `exostrois` (deux ou trois colonnes à pointillés), `exoslibre` (même habillage, contenu libre) : hauteur des lignes, libellé "À vous de jouer" |
| Titres | taille et couleur des `\section` et `\subsection` |
| Schémas | `\compensation` (les flèches en deux temps), `\distrib` (les deux flèches de la distributivité), `\mc` (le code couleur d'une table de multiplication) |
| Étiquettes | `\prog{6}` : la pastille "Programme 6\up{e}" posée à droite d'un titre de partie |

Chaque encadré accepte un titre sur mesure :
`\begin{aretenir}[title={Comment lire cette table}]`.

**Un changement fait là se propage à tous les documents qui chargent le fichier.**

## Un document, deux versions : celle de classe et celle qu'on diffuse

Un document destiné à des élèves porte des informations qui ne doivent pas sortir de
l'établissement : le nom de l'enseignant, celui du collège, la classe, l'année scolaire.
Quand ce même document est partagé à des collègues, ces informations disparaissent, et le
niveau n'apparaît plus que sous forme d'**étiquette de programme** posée sur chaque partie
(`\prog{6}`, `\prog{5}`), qui dit à quelle classe la notion est au programme.

Le piège serait de dupliquer le `.tex` : à la première correction, les deux versions
divergent. La règle est donc **un contenu, deux enveloppes** :

```
_contenu_<sujet>.tex        le corps du document : toutes les sections, rien d'autre.
                            Ne se compile pas seul.
<sujet>.tex                 la version de classe : préambule, \dsheader, auteur,
                            puis \input{_contenu_<sujet>}
<sujet>_partage.tex         la version diffusable : même préambule, aucun nom,
                            aucune classe, puis le même \input
```

Toute correction de contenu se fait dans le fichier `_contenu_…`, **une seule fois**. Les
deux enveloppes ne contiennent que ce qui les distingue : le titre, l'en-tête, et le
paragraphe d'introduction.

Trois points à ne pas oublier dans la version diffusable :

1. `\author{}` et `\date{}` vides, **et** `\hypersetup{pdfauthor={}, pdfcreator={}}` :
   sans cela, hyperref recopie le nom dans les métadonnées du PDF, invisibles à l'écran
   mais lisibles par n'importe qui.
2. Vérifier le résultat sur le PDF compilé, pas sur le source :
   `pdftotext doc.pdf - | grep -i "<nom>"` et `pdfinfo doc.pdf`.
3. Les titres portent l'étiquette via l'argument optionnel :
   `\section[Les fractions]{Les fractions \prog{5}}`. Sans cet argument court, la pastille
   se retrouverait dans le sommaire et dans les signets du PDF.

Exemple en place : `01_2627_4emes_maths/00_calcul_mental/`.

## Règles de tenue de ce dossier

1. Quand une règle est corrigée ou précisée en cours de session, elle est **écrite ici**,
   pas seulement appliquée. Une règle appliquée mais non écrite sera perdue.
2. Les entrées de `pedagogie/erreurs_types.md` sont **datées** (`AAAA-MM-JJ — Titre court`)
   et suivent le template en tête de ce fichier.
3. Une règle qui ne vaut que pour une classe ou un chapitre n'a rien à faire ici : elle
   reste dans le dossier de la classe concernée.

## Arbitrages rendus

Décisions prises en session, pour mémoire.

- **2026-09-06 — Séparateur décimal, par matière.** Virgule en mathématiques
  (`$2{,}4$`), point en physique-chimie (`\SI{7.82}{...}`). Raison : le cours de maths
  parle en permanence du *décalage de la virgule*, un point contredirait ce qui est dit
  au tableau. La règle est écrite dans `latex.md` (sections "Equations et Maths" et
  "Physique") et rappelée dans `google_docs.md`.
- **2026-09-06 — Séparateur de milliers : espace fine, dès 4 chiffres.** `$1\,000$`,
  `$918\,273$`. Jamais de virgule à l'anglaise (`1,000`), qui se lirait comme une
  décimale en français. En physique, `siunitx` s'en charge seul. Ne s'applique pas aux
  années ni aux numéros. Écrite dans `latex.md`.
