# Playbook — Produit de fractions

## Quand utiliser ce playbook

Toute question qui demande de **calculer** un produit de fractions : `\frac{a}{b} \times \frac{c}{d}`, éventuellement avec plus de deux facteurs.

## Méthode

1. **Rappel de la formule** (première occurrence uniquement) : pour multiplier deux fractions, on multiplie les numérateurs entre eux et les dénominateurs entre eux.
2. **Application** : écrire explicitement le produit des numérateurs sur le produit des dénominateurs.
3. **Calcul** du numérateur et du dénominateur.
4. **Simplification éventuelle** (voir `simplification_fractions.md`) et conclusion.

## Exemple rédigé de référence (première occurrence)

```latex
\begin{solution}
On sait que pour multiplier deux fractions, on multiplie les numérateurs
entre eux et les dénominateurs entre eux :
\[
\frac{a}{b} \times \frac{c}{d} = \frac{a \times c}{b \times d}
\]

On applique cette formule :
\[
\frac{2}{3} \times \frac{5}{7} = \frac{2 \times 5}{3 \times 7} = \frac{10}{21}
\]
\end{solution}
```

## Version abrégée (occurrences suivantes)

```latex
\[
\frac{4}{5} \times \frac{3}{8} = \frac{4 \times 3}{5 \times 8} = \frac{12}{40}
\]
```

Puis simplifier si possible (voir playbook `simplification_fractions.md`) :
```latex
\[
\frac{12}{40} = \frac{3 \times \cancel{4}}{10 \times \cancel{4}} = \frac{3}{10}
\]
```

## Produit de plus de deux fractions

Même principe, on multiplie tous les numérateurs entre eux et tous les dénominateurs entre eux :
```latex
\[
\frac{2}{3} \times \frac{5}{7} \times \frac{1}{4}
= \frac{2 \times 5 \times 1}{3 \times 7 \times 4}
= \frac{10}{84}
\]
```
Puis simplification.

## Points de vigilance

- **Laisser visible l'étape intermédiaire** `\frac{2 \times 5}{3 \times 7}` : c'est là qu'on voit la formule appliquée. Ne pas sauter directement à `\frac{10}{21}`.
- **Ne pas confondre avec l'addition** : pour multiplier, **pas besoin** de mettre au même dénominateur. Erreur classique à signaler si l'exercice mélange addition et multiplication de fractions.
- **Toujours simplifier** la fraction finale si possible.
- **Astuce de simplification avant calcul** : si des facteurs communs apparaissent entre un numérateur et un dénominateur, on peut barrer avant de multiplier (cf. `\cancel{...}`). Exemple :
```latex
\frac{3}{8} \times \frac{4}{9}
= \frac{3 \times 4}{8 \times 9}
= \frac{\cancel{3} \times \cancel{4}}{2 \times \cancel{4} \times 3 \times \cancel{3}}
= \frac{1}{6}
```

## Rappel de cours à mobiliser

« Pour multiplier deux fractions, on multiplie les numérateurs entre eux et les dénominateurs entre eux :
$\dfrac{a}{b} \times \dfrac{c}{d} = \dfrac{a \times c}{b \times d}$. »
