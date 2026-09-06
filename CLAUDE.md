# education_suger

Repo d'enseignement : cours, DS/DM, interrogations, corrections et outils.
Mathématiques (6ème en 2025-2026, 4ème en 2026-2027) et physique-chimie.

## Conventions : à lire avant de rédiger quoi que ce soit

**Toutes les conventions de rédaction, de formatage et de pédagogie sont centralisées
dans [`00_conventions/`](00_conventions/README.md).** C'est le point d'entrée unique.

Avant de produire ou de modifier un document destiné aux élèves (LaTeX, Google Doc,
fiche d'exercice, correction, interrogation), lire dans cet ordre :

1. `00_conventions/README.md` — l'index, qui dit quel fichier s'applique au cas présent
2. le fichier de format concerné : `latex.md` ou `google_docs.md`
3. `00_conventions/pedagogie/erreurs_types.md` — l'historique des erreurs déjà commises

Et après **chaque** modification d'un document LaTeX, appliquer
`00_conventions/workflow_latex.md` : compiler deux fois, vérifier le log, puis **ouvrir le
PDF à la page correspondant à la modification** (`synctex` donne la page à partir de la
ligne du source). Ne jamais annoncer un correctif LaTeX sans avoir regardé le rendu.

Quand une règle est corrigée en cours de session, **l'écrire dans `00_conventions/`**,
pas seulement l'appliquer.

## Où vit quoi : la carte des conventions

Les conventions sont **écrites** dans `00_conventions/`. Le style LaTeX est
**implémenté** dans trois fichiers `.sty` à la racine. Les deux sont complémentaires :
on lit les premiers, on modifie les seconds.

| Fichier | Emplacement | Ce que c'est |
|---|---|---|
| `README.md` | `00_conventions/` | **L'index. Point de départ.** Dit quel fichier s'applique à quel cas |
| `latex.md` | `00_conventions/` | Conventions de rédaction et de formatage des documents LaTeX |
| `workflow_latex.md` | `00_conventions/` | **Procédure obligatoire après toute modification d'un `.tex`** : compiler, vérifier, ouvrir le PDF à la page concernée |
| `blocs_de_cours.md` | `00_conventions/` | Les six blocs d'un cours (Théorie, Astuce, Attention, À retenir, Exemple, Exercices), leur traitement visuel et la raison de chaque choix |
| `pieges_techniques.md` | `00_conventions/` | **Erreurs d'outillage qui échouent silencieusement** : shell, regex sur du LaTeX, commandes absentes. À relire avant de modifier par script |
| `google_docs.md` | `00_conventions/` | Conventions des cours en Google Docs (titres, polices, couleurs, encadrés) |
| `redaction_maths.md` | `00_conventions/` | Structure d'un raisonnement maths rédigé : "On sait que / Or / Donc" |
| `redaction_physique.md` | `00_conventions/` | Formules, conversions, application numérique, conclusion |
| `template_latex.tex` | `00_conventions/` | Squelette de départ d'un document LaTeX |
| `pedagogie/langage.md` | `00_conventions/` | Vocabulaire, registre, vouvoiement, infinitif dans les consignes |
| `pedagogie/structure.md` | `00_conventions/` | Séquence des blocs, intro motivante, rappels inter-chapitres |
| `pedagogie/exemples.md` | `00_conventions/` | Choix et progression des exemples |
| `pedagogie/erreurs_types.md` | `00_conventions/` | **Erreurs déjà commises, à relire avant de rédiger** |
| `mypackages.sty` | **racine** | Les packages LaTeX chargés |
| `macros.sty` | **racine** | Raccourcis LaTeX : `\dsheader`, `\fig`, `\trou`, `\ans` |
| `stylecours.sty` | **racine** | Style des cours LaTeX : les 5 encadrés, tableaux d'exercices, palette, schémas |
| `gdoc*.py` | `~/.claude/scripts/` | Application du style aux Google Docs (**hors repo**) |
| `cours_edition/index.md` | `01_2526_6emes_maths/` | Table des URL des Google Docs de cours de 6ème |

**Les fichiers de `pedagogie/` s'appliquent aux deux formats** (ils parlent de ce qu'on
écrit). `latex.md` et les `.sty` ne concernent **que** le LaTeX ; `google_docs.md` et les
scripts `gdoc*.py` ne concernent **que** les Google Docs.

### Les trois `.sty` : pourquoi à la racine, et comment les charger

Un `.sty` n'est pas un programme qu'on lance : c'est un bloc de définitions qu'un
document LaTeX charge au début. Ils sont à la racine parce qu'un `\usepackage` désigne un
chemin **relatif au document**, et que 156 fichiers `.tex` les chargent déjà depuis la
racine, à cinq profondeurs différentes. Les déplacer casserait ces 156 fichiers.

Ordre de chargement obligatoire (ici depuis un dossier à deux niveaux) :

```latex
\usepackage{../../mypackages}   % les packages
\usepackage{../../macros}       % les raccourcis
\usepackage{../../stylecours}   % encadrés, exercices, palette, schémas
```

**Pour changer le rendu d'un encadré dans tous les documents à la fois : `stylecours.sty`,
et nulle part ailleurs.** Le détail de ce qui s'y règle est dans
`00_conventions/README.md`.

## Organisation

| Dossier | Contenu |
|---|---|
| `00_conventions/` | Conventions transverses (voir ci-dessus) |
| `00_pedago/` | Outils, prompts, suivi de classe, formation |
| `01_2526_6emes_maths/` | Année 2025-2026, 6ème : cours, DS/DM, calcul mental |
| `01_2627_4emes_maths/` | Année 2026-2027, 4ème : cours, calcul mental, extraction du manuel |
| `.claude/skills/` | Skills du repo (édition de cours, génération d'interros, corrections) |

## Données élèves

Le repo contient des données personnelles d'élèves. Voir la règle dans le `CLAUDE.md`
global : lister explicitement ce qui est stagé avant tout `git add -A`, et ne jamais
committer un fichier nominatif sans validation explicite.
