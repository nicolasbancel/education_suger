## Prompt N°1 - Retranscription de l'énoncé

[INFORMATIONS IMPORTANTES]
- Mes élèves ont un niveau de 3ème et on entre 14 et 15 ans. Je veux que dans tes réponses, tu t'adaptes à leur niveau, ce qui est inclus dans leur programme.

[TACHE]

Je vais te passer une image qui correspond à un énoncé d'exercice. Je veux que tu restranscrives cet énoncé en latex.

Tu mettras l'énoncé dans une colorbox, en mettant en gras le numéro de l'exercice. Et je veux ensuite que tu insères les réponses aux questions, en étant pédagogue, pour que mes élèves comprennent les étapes du raisonnement

[Contraintes LaTex]
- Je veux que tu sautes une ligne en fin de chaque paragraphe
- Décompose bien les étapes du raisonnement en 1. Méthode 2. Formules 3. Conversions (si nécessaire) 4. Application numérique 5. Conclusion / Interprétation. Ces intitulés doivent être colorés en bleu
- Voici ce à quoi doit ressembler l'en tête
```latex
\setlength{\parindent}{0pt}
\begin{document}

\title{Fiche d'exercice : Masse volumique}
\author{N. Bancel}
\date{Février 2025}

\maketitle

\section{Exercice 1}

\subsection{Problème}
\subsection{Solution}
```

## Prompt N°2 - Copier coller de l'image

[INFORMATIONS IMPORTANTES]
- Mes élèves ont un niveau de 3ème et on entre 14 et 15 ans. Je veux que dans tes réponses, tu t'adaptes à leur niveau, ce qui est inclus dans leur programme.

[TACHE]

Je vais te passer une image qui correspond à un énoncé d'exercice. Je veux que tu restranscrives cet énoncé en latex.

Pour l'énoncé je veux que tu reprennes l'image que je te donne en pièce jointe : je te dirai quel est le chemin pour la trouver.

 Je veux ensuite que tu rédiges les réponses aux questions, en étant pédagogue, pour que mes élèves comprennent les étapes du raisonnement

[Contraintes LaTex]
- Le chemin vers le fichier d'exercice est `04_03_02.jpeg`. L'image doit donc être inséré comme suit 
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{04_03_02.jpeg}
    \caption{Énoncé de l'exercice}
\end{figure}
```
- Je veux que tu inclues la librairie 
`\usepackage{float} % Ajout du package pour l'option H`
- Je veux que tu sautes une ligne en fin de chaque paragraphe
- Décompose bien les étapes du raisonnement en 1. Méthode 2. Formules 3. Conversions (si nécessaire) 4. Application numérique 5. Conclusion / Interprétation. Ces intitulés doivent être colorés en bleu
- Voici ce à quoi doit ressembler l'en tête
```latex
\setlength{\parindent}{0pt}
\begin{document}

\title{Fiche d'exercice : Masse volumique}
\author{N. Bancel}
\date{Février 2025}

\maketitle

\section{Exercice 1}

\subsection{Problème}
\subsection{Solution}
```
