# Playbook — Addition et soustraction de fractions

## Quand utiliser ce playbook

Toute question qui demande d'**additionner** ou de **soustraire** des fractions, quel que soit le nombre de termes.

Si les fractions ont déjà le même dénominateur, sauter directement à « on additionne (ou soustrait) les numérateurs ».

## Structure de rédaction

1. **Rappel du principe** (à expliciter la première fois uniquement) : pour additionner/soustraire deux fractions de dénominateurs différents, il faut d'abord les ramener au même dénominateur.
2. **Choix du dénominateur commun** et justification courte.
3. **Mise au même dénominateur** : une ligne par fraction, en montrant la multiplication haut/bas.
4. **Addition (ou soustraction) des numérateurs** : le dénominateur commun est conservé.
5. **Simplification éventuelle** de la fraction finale (voir `simplification_fractions.md`).
6. **Conclusion** sur la valeur finale.

## Exemple rédigé de référence (addition)

```latex
\begin{solution}
On sait que pour additionner 2 fractions de dénominateurs différents, il
faut d'abord les ramener au même dénominateur. Ici, $12$ fonctionne.

\[
\frac{2}{3} = \frac{2 \times 4}{3 \times 4} = \frac{8}{12}
\qquad\text{et}\qquad
\frac{1}{4} = \frac{1 \times 3}{4 \times 3} = \frac{3}{12}
\]

Une fois les deux fractions au même dénominateur, on additionne les
numérateurs et on garde le dénominateur commun :
\[
\frac{2}{3} + \frac{1}{4} = \frac{8}{12} + \frac{3}{12} = \frac{8 + 3}{12} = \frac{11}{12}
\]
\end{solution}
```

## Exemple rédigé de référence (soustraction)

```latex
\begin{solution}
\[
\frac{5}{6} = \frac{5 \times 2}{6 \times 2} = \frac{10}{12}
\qquad\text{et}\qquad
\frac{3}{4} = \frac{3 \times 3}{4 \times 3} = \frac{9}{12}
\]
\[
\frac{5}{6} - \frac{3}{4} = \frac{10}{12} - \frac{9}{12} = \frac{10 - 9}{12} = \frac{1}{12}
\]
\end{solution}
```

## Version abrégée (questions suivantes)

Une fois que le raisonnement a été exposé une fois dans la correction, on n'explique plus le principe. On enchaîne :
1. Mise au même dénominateur (une ligne par fraction).
2. Addition/soustraction des numérateurs.
3. Simplification éventuelle + conclusion.

## Cas particulier : fractions déjà au même dénominateur

```latex
\[
\frac{3}{7} + \frac{2}{7} = \frac{3 + 2}{7} = \frac{5}{7}
\]
```
Ne pas re-mettre au même dénominateur inutilement.

## Simplification finale

Si la fraction obtenue peut être simplifiée, **la simplifier** en suivant le playbook `simplification_fractions.md` (décomposition en facteurs + `\cancel{...}`). Exemple :

```latex
\frac{6}{12} = \frac{\cancel{6}}{2 \times \cancel{6}} = \frac{1}{2}
```

## Points de vigilance

- **Montrer la multiplication haut ET bas** lors de la mise au même dénominateur : `\frac{2 \times 4}{3 \times 4}`. Ne pas sauter à `\frac{8}{12}` directement.
- **Garder le dénominateur commun** lors de l'addition/soustraction : l'erreur classique est d'additionner aussi les dénominateurs (`\frac{8}{12} + \frac{3}{12} = \frac{11}{24}` ❌). Ne pas hésiter à le signaler dans une boîte `Indication` ou en rouge gras si l'exercice le justifie.
- **Étape intermédiaire `\frac{8 + 3}{12}`** : la laisser visible pour que l'élève voie qu'on additionne bien les numérateurs seuls.
- **Toujours vérifier si la fraction finale se simplifie** — si oui, la simplifier.
- Pour trois fractions ou plus, même principe : on prend un dénominateur commun aux trois.

## Rappels de cours à mobiliser

- « Pour additionner (ou soustraire) deux fractions, elles doivent d'abord avoir le même dénominateur. »
- « Pour additionner deux fractions de même dénominateur, on additionne les numérateurs et on garde le dénominateur commun. »
