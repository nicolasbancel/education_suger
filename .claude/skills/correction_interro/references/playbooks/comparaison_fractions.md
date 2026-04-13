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

Une fois que le raisonnement a été exposé une fois dans la correction, les comparaisons suivantes n'ont plus besoin du discours. On se contente de :

1. Mettre au même dénominateur (une ligne par fraction).
2. Comparer les numérateurs.
3. Conclure sur les fractions d'origine.

```latex
\begin{solution}
\[
\frac{2}{3} = \frac{2 \times 4}{3 \times 4} = \frac{8}{12}
\qquad\text{et}\qquad
\frac{3}{4} = \frac{3 \times 3}{4 \times 3} = \frac{9}{12}
\]
Comme $8 < 9$, on a $\dfrac{2}{3} < \dfrac{3}{4}$.
\end{solution}
```

## Pièges et points de vigilance

- **Bien choisir le dénominateur commun** : si ce n'est pas évident, on peut mentionner qu'on prend le produit des deux dénominateurs, ou un multiple commun plus petit si l'élève peut le voir.
- **Montrer la multiplication haut ET bas** (`\frac{4 \times 5}{9 \times 5}`) — ne pas sauter directement à la fraction réduite. C'est là que les élèves perdent le fil.
- **Ne pas oublier la conclusion finale** sur les fractions d'origine : beaucoup d'élèves s'arrêtent à `20/45 < 36/45` sans revenir à `4/9 < 4/5`.
- **Cas particulier** : si les fractions ont le même numérateur (comme dans l'exemple `4/9` vs `4/5`), on peut signaler en aparté que plus le dénominateur est grand, plus la fraction est petite (mais toujours faire la comparaison au même dénominateur en rédaction principale).

## Rappels de cours à mobiliser

- « Pour comparer deux fractions de même dénominateur, il suffit de comparer leurs numérateurs. »
- « Multiplier le numérateur et le dénominateur d'une fraction par un même nombre non nul ne change pas la valeur de la fraction. »
