# Playbook — Comparaison de fractions

## Quand utiliser ce playbook

Toute question qui demande de **comparer**, **ranger** ou **classer** deux ou plusieurs fractions de **dénominateurs différents**.

Si les fractions ont déjà le même dénominateur, sauter directement à « il suffit de comparer les numérateurs ».

## Structure de la première comparaison (explicite)

La **première fois** qu'une comparaison de fractions apparaît dans la correction, expliciter tout le raisonnement :

1. **Rappel du principe** : « On sait que pour comparer 2 fractions de dénominateurs différents, il faut les ramener au même dénominateur. »
2. **Choix du dénominateur commun** : indiquer lequel et pourquoi (« Ici, 45 fonctionne »).
3. **Mise au même dénominateur** : une ligne par fraction, en montrant la multiplication haut/bas.
4. **Comparaison** : « On sait comparer 2 fractions de même dénominateur : il suffit de comparer les numérateurs. »
5. **Conclusion intermédiaire** sur les fractions équivalentes.
6. **Conclusion finale** sur les fractions d'origine.

## Exemple rédigé de référence

```latex
\begin{solution}
On sait que pour comparer 2 fractions de dénominateurs différents, il faut
les ramener au même dénominateur. Ici, $45$ fonctionne.

\[
\frac{4}{9} = \frac{4 \times 5}{9 \times 5} = \frac{20}{45}
\]

\[
\frac{4}{5} = \frac{4 \times 9}{5 \times 9} = \frac{36}{45}
\]

On sait comparer 2 fractions de même dénominateur : il suffit de comparer
les numérateurs. Donc
\[
\frac{20}{45} < \frac{36}{45}
\]
Donc
\[
\frac{4}{9} < \frac{4}{5}.
\]
\end{solution}
```

## Version abrégée (questions suivantes)

Une fois que le raisonnement a été exposé une fois dans la correction, les comparaisons suivantes n'ont plus besoin du discours. Format à suivre, en **trois lignes aérées** avec `\\` :

1. **Ligne 1** : « On met au même dénominateur. » suivi de la ou des transformations inline.
2. **Ligne 2** : comparaison des fractions de même dénominateur avec une justification courte entre parenthèses : `(même dénominateur, et 6 > 5)`.
3. **Ligne 3** : conclusion avec « donc » et retour aux fractions d'origine.

### Cas où une seule fraction doit être transformée (dénominateur de l'une est multiple de l'autre)

```latex
\begin{solution}
  On met au même dénominateur :
  \[
    \dfrac{3}{4} = \dfrac{3 \times 2}{4 \times 2} = \dfrac{6}{8}
  \]
  Les deux fractions ont le même dénominateur, et $6 > 5$, donc :
  \[
    \dfrac{6}{8} > \dfrac{5}{8}
    \qquad\text{c'est-à-dire}\qquad
    \dfrac{3}{4} > \dfrac{5}{8}.
  \]
\end{solution}
```

### Cas où les deux fractions doivent être transformées

```latex
\begin{solution}
  On met au même dénominateur. Ici, $7 \times 8 = 56$ fonctionne.
  \[
    \dfrac{4}{7} = \dfrac{4 \times 8}{7 \times 8} = \dfrac{32}{56}
    \qquad\text{et}\qquad
    \dfrac{5}{8} = \dfrac{5 \times 7}{8 \times 7} = \dfrac{35}{56}
  \]
  Les deux fractions ont le même dénominateur, et $32 < 35$, donc :
  \[
    \dfrac{32}{56} < \dfrac{35}{56}
    \qquad\text{c'est-à-dire}\qquad
    \dfrac{4}{7} < \dfrac{5}{8}.
  \]
\end{solution}
```

**Règle** : **toute fraction va en display `\[ ... \]`**, même une simple comparaison. La phrase de texte entre les deux blocs display ne contient que des entiers (« $32 < 35$ », « même dénominateur »). La comparaison des fractions équivalentes ET la conclusion sur les fractions d'origine tiennent dans un seul bloc display, reliés par `\qquad\text{c'est-à-dire}\qquad`.

## Pièges et points de vigilance

- **Bien choisir le dénominateur commun** : si ce n'est pas évident, on peut mentionner qu'on prend le produit des deux dénominateurs, ou un multiple commun plus petit si l'élève peut le voir.
- **Montrer la multiplication haut ET bas** (`\frac{4 \times 5}{9 \times 5}`) — ne pas sauter directement à la fraction réduite. C'est là que les élèves perdent le fil.
- **Ne pas oublier la conclusion finale** sur les fractions d'origine : beaucoup d'élèves s'arrêtent à `20/45 < 36/45` sans revenir à `4/9 < 4/5`.
- **Cas particulier** : si les fractions ont le même numérateur (comme dans l'exemple `4/9` vs `4/5`), on peut signaler en aparté que plus le dénominateur est grand, plus la fraction est petite (mais toujours faire la comparaison au même dénominateur en rédaction principale).

## Rappels de cours à mobiliser

- « Pour comparer deux fractions de même dénominateur, il suffit de comparer leurs numérateurs. »
- « Multiplier le numérateur et le dénominateur d'une fraction par un même nombre non nul ne change pas la valeur de la fraction. »
