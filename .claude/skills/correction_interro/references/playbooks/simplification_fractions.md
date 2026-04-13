# Playbook — Simplification de fractions

## Quand utiliser ce playbook

Toute question qui demande de **simplifier**, **réduire** ou **rendre irréductible** une fraction.

## Structure de rédaction

1. **Décomposer** le numérateur et le dénominateur en produits de facteurs, en faisant apparaître les facteurs communs.
2. **Barrer** les facteurs communs en haut et en bas avec `\cancel{...}`.
3. **Conclure** en donnant la fraction simplifiée.

## Exemple rédigé de référence

```latex
\begin{solution}
On décompose le numérateur et le dénominateur en faisant apparaître les
facteurs communs, puis on barre les facteurs qui apparaissent à la fois
en haut et en bas :
\[
\frac{24}{36}
= \frac{2 \times 2 \times 2 \times 3}{2 \times 2 \times 3 \times 3}
= \frac{\cancel{2} \times \cancel{2} \times 2 \times \cancel{3}}{\cancel{2} \times \cancel{2} \times 3 \times \cancel{3}}
= \frac{2}{3}
\]
\end{solution}
```

## Variante avec un seul facteur commun visible

Quand la simplification repose sur un unique facteur commun évident, on peut rester très direct :
```latex
\[
\frac{15}{20}
= \frac{3 \times \cancel{5}}{4 \times \cancel{5}}
= \frac{3}{4}
\]
```

## Points de vigilance

- **Toujours montrer la décomposition** avant de barrer. Ne pas passer directement de `24/36` à `2/3` — l'élève doit voir d'où viennent les facteurs.
- **Barrer en haut ET en bas** pour chaque facteur commun annulé : `\cancel{2}` au numérateur ET `\cancel{2}` au dénominateur.
- **Vérifier que la fraction obtenue est irréductible** : les facteurs restants au numérateur et au dénominateur n'ont plus aucun facteur commun.
- Si plusieurs facteurs sont communs, on peut les barrer tous dans la même étape (pas besoin d'un passage intermédiaire par facteur).

## Rappel de cours à mobiliser

« Diviser le numérateur et le dénominateur d'une fraction par un même nombre non nul ne change pas la valeur de la fraction. Barrer un facteur commun en haut et en bas revient à diviser par ce facteur. »

## Prérequis LaTeX

La commande `\cancel{...}` est fournie par le package `cancel`, qui doit être chargé (typiquement via `mypackages.sty`). Si `\cancel` n'est pas disponible dans le document cible, signaler à l'utilisateur plutôt que de chercher une alternative.
