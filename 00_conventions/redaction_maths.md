- Dès qu'il est nécessaire de justifier, je veux que la structure du raisonnement soit 
    - "On sait que" (on liste les hypothèse utiles)
    - "Or" (on fait appel à la propriété importante)
    - "Donc"
- Je veux que la partie formule soit toujours présente (en respectant quand même le niveau des élèves)

Exemple : si je connais 2 angles sur les 3 dans un triangle, je veux voir 
```latex
$\widehat(ABC) + \widehat(ACB) + \widehat(BAC) = 180$
$\widehat(ABC) = 180 - \widehat(ACB) - \widehat(BAC)$
```
Et ensuite tu peux passer à l'application numérique où tu remplaces $\widehat(ACB)$ et $\widehat(BAC)$ par les valeurs connues grâce à l'énoncé ou aux questions précédentes.

## Barrer des termes qui se simplifient

Convention : **`\cancel{...}`** du package `cancel` (chargé par `mypackages.sty`), appliqué
au **même terme en haut et en bas**. Le lecteur voit d'un coup d'œil quel facteur disparaît
et pourquoi.

Origine : le cours de physique de 3ème (`01_2425_3ème_CI_pc/methodes/methodes.tex`), où
elle sert à isoler une variable dans une formule.

```latex
\rho \cdot V = \frac{m}{\cancel{V}} \cdot \cancel{V}

\frac{\cancel{\rho} \cdot V}{\cancel{\rho}} = \frac{m}{\rho}
```

### Ne pas utiliser `\cancelto`

`\cancelto{reste}{terme}` barre le terme **et écrit le quotient en petit à côté de la
barre**. Dès qu'il y a deux simplifications sur la même ligne, les restes se superposent
aux fractions voisines et deviennent illisibles. Écarté le 2026-09-06 après constat sur le
document de calcul mental de 4ème.

### Ne pas écrire le diviseur au-dessus du signe égal

`\overset{\div\,2}{=}` (le « ÷ 2 » posé sur le signe égal) est également écarté. C'est une
notation d'annotation, pas une écriture mathématique : le lecteur ne voit pas *sur quoi*
porte la division, et l'égalité elle-même se retrouve surchargée. Une simplification de
fraction s'écrit toujours avec `\cancel`, y compris quand elle se fait en plusieurs
étapes. Relevé le 2026-09-06 sur le document de calcul mental.

```latex
% NON
\frac{24}{36} \overset{\div\,2}{=} \frac{12}{18} \overset{\div\,2}{=} \frac{6}{9}

% OUI
\frac{24}{36} &= \frac{\cancel{2} \times 12}{\cancel{2} \times 18} = \frac{12}{18} \\
              &= \frac{\cancel{2} \times 6}{\cancel{2} \times 9}   = \frac{6}{9}
```

### Simplification partielle : décomposer d'abord

Quand deux nombres ne se simplifient pas complètement (par exemple $4$ avec $8$),
**décomposer avant de barrer**, pour faire apparaître le facteur commun de part et
d'autre. On se ramène ainsi toujours au cas « le même terme en haut et en bas », et on
n'a jamais besoin d'écrire un reste.

```latex
\frac{4}{9} \times \frac{3}{8}
  &= \frac{4 \times 3}{9 \times 8} \\
  &= \frac{4 \times 3}{(3 \times 3) \times (4 \times 2)}
     &&\text{car } 9 = 3 \times 3 \text{ et } 8 = 4 \times 2 \\
  &= \frac{\cancel{4} \times \cancel{3}}{(\cancel{3} \times 3) \times (\cancel{4} \times 2)} \\
  &= \frac{1}{3 \times 2} = \frac{1}{6}.
```

Bénéfice pédagogique au passage : l'élève voit **pourquoi** la simplification est légitime,
au lieu de constater un résultat apparu à côté d'une barre.
