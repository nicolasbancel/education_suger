Je suis professeur de Physique Chimie et je fais un cours à des 3ème qui ont 13 ans. Je veux leur expliquer des méthodes pour bien faire un raisonnement scientifique.

Ecris moi un cours en format Latex en 3 parties sur
1. La notation scientifique et les chiffres significatifs
2. Ajoute des rappels sur les notions mathématiques d'opérations sur les puissances

## Prompt notation scientifique

J'ai une macro \trou{}{} qui en 1er argument prend la réponse à une question et en 2nd argument détermine un espace vide pour que mes étudiants puissent écrire les réponses par eux-mêmes.

Je veux que tu m'écrives un exercice où les choses à convertir sont dans la colonne de gauche, et les réponses ou corrections sont dans la colonne de droite.

Par exemple : 

begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{3cm} >{\raggedright\arraybackslash}X}
  \toprule
  {\textbf{Nombre}} & {\textbf{Nombre de chiffres significatifs}} \\
  \midrule
  {0,0450} & {\trou{3 chiffres significatifs (4, 5 et le dernier 0 après le point décimal)}{\ndots[20]}} \\
  \midrule
  {3,200} & {\trou{4 chiffres significatifs (3, 2, 0, et 0, car les zéros à droite d'un nombre décimal sont significatifs).}{\ndots[20]}} \\
  \midrule
  {500} & {\trou{1 chiffre significatif (le 5, car les zéros à droite sans point décimal ne sont pas significatifs)}{\ndots[20]}} \\
  \midrule
  {0,0032} & {\trou{2 chiffres significatifs (3 et 2 ; les zéros à gauche ne sont pas significatifs)}{\ndots[20]}} \\
  \midrule
  {7,0000} & {\trou{5 chiffres significatifs (7 et les quatre zéros après la virgule).}{\ndots[20]}} \\
  \midrule
  {123,45} & {\trou{5 chiffres significatifs (tous les chiffres sont significatifs dans ce nombre)}{\ndots[20]}} \\
  \midrule
  {$6,02 \times 10^{23}$} & {\trou{3 chiffres significatifs (6, 0, et 2 ; en notation scientifique, seuls les chiffres avant le x10 sont significatifs)}{\ndots[20]}} \\
  \bottomrule
\end{tabularx}

Sur ce format là, écris moi 7 questions de nombres qu'il faut écrire en notation scientifique
