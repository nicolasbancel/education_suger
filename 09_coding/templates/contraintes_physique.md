
**General**
- Utilise des balises `\begin{questions}` pour chaque répondre à chaque question
- Tu écriras la correction dans une balise `\begin{solution}`

**Contraintes Latex**
- Je veux que tu utilises `begin{compactitem}` et pas `begin{itemize}`
- Tu peux utiliser des balises `\subsection*{}` pour bien séparer les questions de l'exercice
- Pour écrire des valeurs numériques avec des unités, je veux que tu utilises la balise `\SI{}{}`. Par exemple : `\SI{7.82}{g\per\cubic\centi\meter}`
-  Tu utiliseras les unités de fraction avec ce mode : `\unit[per-mode = symbol]{\meter\per\second}`
- Quand tu écris des formules, je veux que tu respectes un format où tu énonces la formule, et tu listes et définis chaque variable.
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
- Quand tu écris des équations les unes à la suite des autres, je veux que ces équations soient alignées

**Contraintes de raisonnement**
- Je veux que tu décomposes tes raisonnements en 3 parties 
  1. Raisonnement avec formules mathématiques (avec des lettres)
  2. Conversions dans les bonnes unités
  3. Application numérique (ici, tu peux mettre des nombres, mais sans les unités. Seul le résultat final inclut les unités).
  4. Conclusion / Interprétation
- Ne le fais que si c'est vraiment pertinent de le faire. Si le raisonnement est très rapide, pas besoin de surcharger la correction
