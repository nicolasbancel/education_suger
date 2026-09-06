# Général - Formatting

- **Séparateur décimal : il dépend de la matière.** Virgule en mathématiques, point en physique-chimie. Voir les sections "Général - Equations et Maths" et "Physique" ci-dessous.
- Utilise des balises \begin{solution} et \end{solution} pour encadrer la réponse
- Si tu veux énumérer des points, utilise des balises \begin{compactenum}
- Si tu veux lister des points, utilise des balises \begin{compactitem}
- S'il y a des sous-questions, je veux que tu utilises \begin{part}

- Nomme le titre des exercices dans une balise \section
- Le screenshot de l'exercice doit lui aussi être présent, en utilisant la fonction \fig{}{}{} où le 1er argument est le % de linewidth (tu peux utiliser 0,6 par défaut), le 2ème argument est le path vers l'exercice (prends exactement celui qui t'est fourni dans l'énoncé), le 3ème argument est le titre de la figure.
- Suis les mêmes libraires, façons d'écrire (les vecteurs, formules chimiques etc) que dans l'énoncé

# Général - Rédaction

- Mes élèves ne sont pas toujours à l'aise avec les calculs donc je veux que tu décomposes tous les calculs
- Ecris les accents normalement : "périodique" plutôt que "p\'eriodique". "être déduit" plutôt que "\^etre d\'eduit".

# Général - Equations et Maths

- **Nombres décimaux : virgule.** Écrire `$2{,}4$` et non `$2.4$`. Les accolades autour de la virgule sont obligatoires : en mode mathématique, LaTeX traite la virgule comme une ponctuation et ajoute une espace après, ce qui donnerait `2, 4`. Les accolades la neutralisent.
- **Pourquoi la virgule en maths** : le cours parle en permanence du *décalage de la virgule* (multiplier ou diviser par 10, 100, 1 000). Un point à l'écran contredirait ce qui est dit et écrit au tableau.
- **Séparateur de milliers : espace fine, dès 4 chiffres.** Écrire `$1\,000$`, `$3\,974$`, `$918\,273$`. Jamais `$1000$` collé, et surtout jamais `$1,000$` (format anglais : en français cette virgule se lit comme une décimale). En mode mathématique, `\,` produit l'espace fine insécable de la typographie française.
- Le séparateur de milliers ne s'applique **pas** aux nombres qui ne sont pas des quantités : une année (`en 2026`), un numéro de page, un identifiant.

- Les formules mathématiques centrées doivent utiliser [\ xxx \] tandis que au sein d'une même ligne, je veux que tu utilises $ xxx $ et pas (\ xxx \).
- Quand plusieurs équations se suivent, utilise le mode \begin{align*} \end{align*}
- Je veux aussi que tu décomposes un raisonnement scientifique en plusieurs étapes : formules, conversions, application numérique. Ne note pas les unités dans l'application numérique.
- Quand tu écris des équations les unes à la suite des autres, je veux que ces équations soient alignées

```latex
% align* will not number the equations
  \begin{align}
    AE &= \sqrt{(1-0)^2 + (0 - 0)^2 + (0 - (-1))^2} \\
    AE &= \sqrt{(1)^2 + (0)^2 + (1)^2} \\
    AE &= \sqrt{2} \\
  \end{align}
```

# Chimie

- Pour les formules de molécules, tu utiliseras des formes du type de \ce{NH3}

# Physique

- **Nombres décimaux : point.** Écrire `\SI{7.82}{...}` et non `\SI{7,82}{...}`. C'est la convention du package `siunitx` et celle des sciences expérimentales.
- **Séparateur de milliers : rien à faire.** `siunitx` insère l'espace fine tout seul : `\SI{47047}{\meter}` s'affiche `47 047 m`. Ne pas écrire `\,` à la main dans un `\SI{}{}`.

- Pour écrire des valeurs numériques avec des unités, je veux que tu utilises la balise `\SI{}{}`. Par exemple : `\SI{7.82}{g\per\cubic\centi\meter}`
-  Tu utiliseras les unités de fraction avec ce mode : \unit[per-mode = symbol]{\meter\per\second}
- Quand tu écris des formules et que tu veux mettre des unités, je veux que tu respectes ce format. 

- Quand tu écris des formules et que tu veux mettre des unités, je veux que tu respectes ce format. 
```
  Contexte : La vitesse d'un objet peut se calculer en mesurant en distance, et en déterminant le temps qu'il a fallu à cet objet pour parcourir cette distance. Sa formule s'écrit
  \[
  v = \frac{d}{t}
  \]
  où 

  \begin{addmargin}[4em]{1em}
    \begin{compactitem}
        \item [v]: représente la vitesse de l'objet
        \item [d]: représente la distance parcourue
        \item [t]: représente le temps écoulé pour que l'objet parcourt la distance
    \end{compactitem}
    \end{addmargin}
```


