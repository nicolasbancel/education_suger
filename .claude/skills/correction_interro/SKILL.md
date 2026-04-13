---
name: correction_interro
description: Génère la correction d'une interrogation de Mathématiques de 6ème au format LaTeX, en respectant des contraintes pédagogiques et typographiques précises.
---

## Quand activer ce skill

Activer dès que l'utilisateur demande :
- de rédiger / générer / compléter la **correction** d'une interro, d'un DS ou d'un DM de 6ème
- de remplir les blocs `\begin{solution} ... \end{solution}` d'un fichier `.tex` existant
- de relire / corriger une correction déjà écrite pour la remettre aux normes

## Étapes obligatoires avant de rédiger

1. **Lire les références** (ordre recommandé) :
   - `references/latex_patterns.md` — règles typographiques et LaTeX
   - `references/redaction_patterns.md` — style pédagogique, structure des justifications
   - `references/macros_disponibles.md` — raccourcis à réutiliser (`\justifier`, `\fig`, `\textrr`, environnement `Indication`, etc.)
   - `references/playbooks/README.md` — index des playbooks par type d'exercice (voir section « Playbooks par type d'exercice » plus bas)
2. **Lire au moins un corrigé de référence** pour caler le ton :
   - `01_2526_6emes_maths/00_ds_dm/interro_2/6eme_interro_2_correction.tex`
   - `01_2526_6emes_maths/00_ds_dm/interro_3/6eme_interro_3_correction.tex` (référence principale, très complet)
   - `01_2526_6emes_maths/00_ds_dm/interro_4/6eme_interro_4.tex` (utilise `Indication`, `\fig`, `\justifier`)
   - `01_2526_6emes_maths/00_ds_dm/interro_5/6eme_interro_5.tex`
3. **Vérifier les macros** dans `01_2526_6emes_maths/macros.sty` si une balise semble custom.
4. **Lire le fichier `.tex` cible** pour comprendre questions et barème avant de remplir les solutions.

Les fichiers du dossier `01_2526_6emes_maths/00_ds_dm/` sont la **source de vérité**. En cas de conflit entre une règle `references/*` et ce qu'un corrigé validé montre, signaler la contradiction à l'utilisateur plutôt que trancher seul.

## Règles structurelles non négociables

- Les solutions vont dans des blocs `\begin{solution} ... \end{solution}`. Elles sont rendues automatiquement **en bleu** grâce à `\SolutionEmphasis{\color{blue}}` en préambule. Ne jamais ajouter `\color{blue}` à la main.
- Ne pas toucher au préambule (`\documentclass`, imports, macros) sauf demande explicite.
- Un calcul = **un seul** `align*` (règle détaillée dans `references/latex_patterns.md` §2).
- Les questions marquées `\justifier` ou `[Justifier]` attendent une rédaction structurée **« On sait que / Or / Donc »** (détails dans `references/redaction_patterns.md` §1).

## Résumé ultra-court des contraintes

Si tu n'as le temps de ne lire qu'une chose, retiens :

- **Listes** : `compactitem`, `compactenum` (jamais `itemize`).
- **Calculs** : un seul `align*`, commentaires à droite via `&& \text{...}`.
- **Maths inline** : `$...$` uniquement.
- **Apostrophes** : droites ASCII `'`. **Guillemets** : droits `"..."`.
- **Couleurs** : rouge pour les avertissements, bleu automatique pour les solutions.
- **Indication** : boîte verte `\begin{Indication}...\end{Indication}` pour les critères « ce qui était attendu » et les mises en garde.
- **VF** : réponse `[VRAI]`/`[FAUX]` en gras rouge **avant** la justification, conclusion en gras **après**.
- **Justifications** : « On sait que … Or … Donc … » — ancrer chaque hypothèse dans l'énoncé ou le codage.
- **Figures** : `\fig{largeur}{fichier}{légende}` ou bloc `figure[H]` complet avec `\captionsetup{labelformat=empty}`.

## Playbooks par type d'exercice

Pour certains types de questions, un playbook dédié précise la structure de rédaction attendue (formulation type, exemple rédigé, pièges, version abrégée…). **Lire le playbook correspondant EN PLUS** des références générales quand tu identifies le type.

| Type de question | Déclencheurs | Playbook |
|---|---|---|
| Comparaison de fractions | « comparer », « ranger », « classer » des fractions ; dénominateurs différents | `references/playbooks/comparaison_fractions.md` |
| Simplification de fractions | « simplifier », « réduire », « rendre irréductible » une fraction | `references/playbooks/simplification_fractions.md` |
| Addition / soustraction de fractions | « calculer », « additionner », « soustraire » deux fractions | `references/playbooks/addition_soustraction_fractions.md` |
| Décomposition entier + fraction < 1 | « décomposer », « écrire sous la forme d'un entier et d'une fraction inférieure à 1 » | `references/playbooks/decomposition_entier_fraction.md` |
| Produit de fractions | « calculer », « multiplier » deux fractions | `references/playbooks/produit_fractions.md` |

Index complet et instructions pour ajouter un nouveau playbook : `references/playbooks/README.md`.

## Workflow recommandé

1. Lire le fichier `.tex` cible (questions + barème).
2. Identifier pour chaque question : définition / calcul / VF à justifier / construction géométrique / justification géométrique / problème ouvert. Adapter la verbosité en conséquence (voir tableau dans `references/redaction_patterns.md` §9).
3. Remplir les blocs `\begin{solution}` un par un.
4. Ajouter des boîtes `Indication` quand des critères ou mises en garde sont utiles.
5. **Relecture finale** : apostrophes ASCII ? guillemets droits ? `compactitem` partout ? `align*` complet ? pas de `\color{blue}` manuel ? réponse VF en gras rouge d'abord puis conclusion en gras ?
