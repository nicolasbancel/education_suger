# Playbook — Simplification de fractions

## Quand utiliser ce playbook

Toute question qui demande de **simplifier**, **réduire** ou **rendre irréductible** une fraction.

## Deux méthodes équivalentes à présenter

Pour simplifier une fraction, deux écritures sont acceptées et pédagogiquement utiles. **La première fois** qu'une simplification apparaît dans la correction, **montrer les deux méthodes côte à côte** dans un `compactitem` pour que l'élève voie qu'elles donnent le même résultat.

- **Méthode 1 — division au numérateur et au dénominateur** par le facteur commun.
- **Méthode 2 — décomposition en produits de facteurs** + `\cancel{...}` pour barrer les facteurs communs.

## Structure de la première simplification (version complète — deux méthodes)

```latex
\begin{solution}
On peut simplifier la fraction de deux manières équivalentes.

\begin{compactitem}
  \item \textbf{Méthode 1} (division par le facteur commun) : $\dfrac{12}{18} = \dfrac{12 \div 6}{18 \div 6} = \dfrac{2}{3}$ \\
  \item \textbf{Méthode 2} (décomposition en facteurs et simplification) : $\dfrac{12}{18} = \dfrac{\cancel{6} \times 2}{\cancel{6} \times 3} = \dfrac{2}{3}$
\end{compactitem}
\end{solution}
```

Ici l'inline `$...$` est acceptable car chaque méthode est un item d'une liste — c'est l'exception au principe « privilégier le display ».

## Version abrégée (simplifications suivantes)

Une fois les deux méthodes exposées, les simplifications suivantes n'ont plus besoin de montrer les deux. **Choisir la plus lisible** selon le cas — en général la méthode 2 (`\cancel{...}`) quand les facteurs sont clairs, la méthode 1 (division) quand le facteur commun est évident.

```latex
\begin{solution}
\[
  \frac{35}{49} = \frac{\cancel{7} \times 5}{\cancel{7} \times 7} = \frac{5}{7}
\]
\end{solution}
```

ou :

```latex
\begin{solution}
\[
  \frac{35}{49} = \frac{35 \div 7}{49 \div 7} = \frac{5}{7}
\]
\end{solution}
```

## Points de vigilance

- **Toujours montrer l'étape intermédiaire** (décomposition ou division) avant le résultat. Ne pas passer directement de `12/18` à `2/3` — l'élève doit voir d'où vient la simplification.
- **Pour la méthode 2** : barrer en haut ET en bas le même facteur (`\cancel{6}` au numérateur ET au dénominateur). Et bien écrire la fraction sous forme produit (`6 \times 2`) et non somme.
- **Vérifier que la fraction obtenue est irréductible** : les facteurs restants au numérateur et au dénominateur n'ont plus aucun facteur commun.
- **Plusieurs facteurs communs** : on peut les barrer tous dans la même étape (`\frac{\cancel{2} \times \cancel{3} \times 5}{\cancel{2} \times \cancel{3} \times 7}`).

## Rappel de cours à mobiliser

« Diviser le numérateur et le dénominateur d'une fraction par un même nombre non nul ne change pas la valeur de la fraction. Barrer un facteur commun en haut et en bas dans une écriture sous forme de produit revient à diviser par ce facteur. »

## Prérequis LaTeX

La commande `\cancel{...}` est fournie par le package `cancel`, qui doit être chargé (typiquement via `mypackages.sty`). Si `\cancel` n'est pas disponible dans le document cible, signaler à l'utilisateur plutôt que de chercher une alternative.
