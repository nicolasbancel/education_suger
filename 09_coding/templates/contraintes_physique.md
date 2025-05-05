
**General**
- Utilise des balises \begin{questions} pour chaque répondre à chaque question
- Tu écriras la correction dans une balise \begin{solution}

**Equations chimiques**
- Pour les formules de molécules, tu utiliseras des formes du type de \ce{NH3}
- 

**Contraintes Latex**
- Je veux que tu utilises `begin{compactitem}` et pas `begin{itemize}`
- Si tu délimites le raisonnement de ta correction avec des sections, je veux que ce soit des `subsection`
- 
- Pour écrire des valeurs numériques avec des unités, je veux que tu utilises la balise `\SI{}{}`. Par exemple : `\SI{7.82}{g\per\cubic\centi\meter}`
-  Tu utiliseras les unités de fraction avec ce mode : \unit[per-mode = symbol]{\meter\per\second}
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
- Quand tu écris des équations les unes à la suite des autres, je veux que ces équations soient alignées

**Contraintes de raisonnement**
- Je veux que tu décomposes tes raisonnements en 3 parties 
  - Raisonnement avec formules mathématiques (avec des lettres)
  - Conversions dans les bonnes unités
  - Application numérique (ici, tu peux mettre des nombres, mais sans les unités. Seul le résultat final inclut les unités). Tu veilleras à respecter les bons nombres de chiffres significatifs
  - Conclusion / Interprétation
- Ne le fais que si c'est vraiment pertinent de le faire. Si le raisonnement est très rapide, pas besoin de surcharger la correction
