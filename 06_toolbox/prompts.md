# Logbook

## Prompt #2

Je fais des appréciations très personnalisées à mes élèves pour chacune de leurs interrogations, et les log dans des fichiers json. Le json est constituté de 5 clés : 
- name : le nom de l'interrogation (qui résume ce sur quoi elle porte)
- eleve : le prénom de l'élève
- general_maitrise : ce qui est maitrisé par ma classe sur cette interrogation
- general_retravailler : ce qui doit être retravaillé par ma classe
- transcript_eleve : mon compte rendu sur l'élève

Basé sur ces informations, je veux que tu me génères une fiche de 10 exercices qui adressent précisément les sujets sur lesquels mon élève doit progresser. Pour un niveau 3ème en Physique Chimie.

Le format de la fiche d'exercice doit être en LaTex, et doit comporter plusieurs sections : 
- Section 1 : les notions sur lesquelles la fiche d'exercices a vocation à faire travailler
- Section 2 : les exercices
- Section 3 : la correction des exercices

Tu devras suivre ce format : 

\documentclass[a4paper,12pt]{article}

\setlength{\parindent}{0pt}

\begin{document}

\title{Fiche d'exercices - ### INTRODUIRE ICI LE PRENOM DE L'ELEVE ###}
\author{N. Bancel}
\date{}
\maketitle

\section{Notions travaillées dans cette fiche d'exercices}

\section{Exercices}

\section{Corrigés}

\end{document}

## Prompt #1

Je fais des appréciations très personnalisées à mes élèves pour chacune de leurs interrogations, et les log dans des fichiers json. Le json est constituté de 5 clés : 
- name : le nom de l'interrogation (qui résume ce sur quoi elle porte)
- eleve : le prénom de l'élève
- general_maitrise : ce qui est maitrisé par ma classe sur cette interrogation
- general_retravailler : ce qui doit être retravaillé par ma classe
- transcript_eleve : mon compte rendu sur l'élève

Basé sur ces informations, je veux que tu me génères une fiche de 5 exercices qui adressent précisément les sujets sur lesquels mon élève doit progresser. Pour un niveau 3ème en Physique Chimie.

Le format de la fiche d'exercice doit être en LaTex, et suivre ce format : 

\documentclass[a4paper,12pt]{article}

\setlength{\parindent}{0pt}

\begin{document}

\title{Fiche d'exercices - ### INTRODUIRE ICI LE PRENOM DE L'ELEVE ###}
\author{N. Bancel}
\date{}
\maketitle

### INTRODUIRE ICI LES EXERCICES ###

\end{document}


# Corrigé exercices

Je vais te passer une image qui correspond à un énoncé d'exercice. Je veux que tu restranscrives cet énoncé en latex 

Tu mettras l'énoncé dans une colorbox, en mettant en gras le numéro de l'exercice. Et je veux ensuite que tu insères les réponses aux questions, en étant pédagogue, pour que mes élèves de 1ère comprennent les étapes du raisonnement


# Format corrigé Google Sheet

_Pour remplir ce document : [[DS] Notes élèves et suivi note par question](https://docs.google.com/spreadsheets/d/1vHl52CN3iHYNIzD0KX6STDxoTg3C3oFMOxQwCoV8Erw/edit?gid=502728493#gid=502728493)

Je veux pouvoir corriger mes copies en notant dans un excel combien de points mes élèves ont eu sur chaque réponse. A partir de l'énoncé du contrôle que je donne (en latex en dessous de ce paragraphe), je veux que tu me génères un tableau avec les colonnes suivantes : 

- Partie
- N° question
- Sous-question
- Barême
- Thème

où
- Partie correspond à une partie ou au numéro d'un exercice
- N° question correspond au numéro de la question
- Sous-question correspond au numéro ou à la lettre de la sous question (a, b, c par exemple)
- Barême correspond au nombre de points alloués à la question
- Thème : je veux que tu identifies le thème qu'adresse le sujet de la question / ce qui est testé. Le thème ne doit pas être une paraphrase du contenu de la question mais plutôt une catégorie, dy type "Vocabulaire atome / molécule", ou "Equilibrage équation chimique", "Identification réactifs et produits", "Opérations mathématiques"

Et les autres colonnes doivent correspondre au prénom de chacun de mes élèves :


Voici l'énoncé de mon contrôle : 



- Clem
- Marjane
- Milena
- Katia
- Milan
- Margaux

- Naël
- Faustine
- Isaure
- Lou
- Alina
- Charles
- Sadra
- Alexia
- Thais
- Valentine
- Kavya


# Contrôle de Maths


## Prompt correction de contrôle

Voici le contrôle que j'ai donné à ma classe de 1ère STD2A. Je veux que tu me rédiges un corrigé, en répondant à chaque question entre les lignes. Sois très explicite dans les réponses pour qu'ils puissent se servir de ta correction dans leurs prochaines révisions. Le format de sortie doit être en LaTex

Contraintes : 
- Tu utiliseras \begin{itemize}[noitemsep] quand tu voudras faire des bullet points
- Mets des phrases en couleur (bleu ou rouge) quand elles sont très importantes
- Je veux que tu utilises les mêmes librairies que dans l'énoncé : \ce ou \chemfig
- Suis les mêmes libraires, façons d'écrire (les vecteurs, formules chimiques etc) que dans l'énoncé
- mes élèves ne sont pas toujours à l'aise avec les calculs donc je veux que tu décomposes tous les calculs

Contraintes sur le programme. Mes élèves ne connaissent pas
- les démonstrations par récurrence
- les calculs de déterminants pour les fonctions

L'image à laquelle fait référence l'exercice de géométrie dans l'espace est en pièce jointe


## Prompt rédaction de contrôle


En suivant le format ci-dessous, je veux que tu rédiges un contrôle de 30 minutes pour mes 1ères. Ils sont censés maitriser les notions suivantes : 

- Savoir calculer les termes d'une suite (d'une suite définie de manière fonctionnelle, et définie de manière récurrente)
- Connaître les définitions d'une suite géométrique, et d'une suite arithmétique. 
- Reconnaître une suite arithmétique, ou une suite géométrique (montrer qu'une suite peut s'écrire sous la forme U(n+1) = U(n) + r ou U(n+1) = q * U(n)
- Etre capable de démontrer qu'une suite est croissante, ou décroissante.

<format>
\documentclass{exam}
\usepackage{../../mypackages}
\usepackage{../../macros}

\title{Interro N°1 - Chimie organique}
\author{N. Bancel}
\date{Novembre 2024}

\begin{document}

\textbf{Collège Lycée Suger}
\hfill
\textbf{Physique-Chimie} \\

\textbf{Année 2024-2025}
\hfill
\textbf{1ères STD2A} \par

{\let\newpage\relax\maketitle}

\begin{center}
\textbf{\textcolor{red}{Durée : 30 minutes. La calculatrice n'est pas autorisée}} \\
\textbf{\textcolor{red}{Une réponse donnée sans justification sera considérée comme fausse.}} \\

\end{center}

\section*{Partie 1 : Blablabla}

\begin{questions}
  \question[1] Blablabla
  \begin{parts}
    \part[0.5] D'un alcane
    \part[0.5] D'un alcène
\end{parts}

\end{questions}
\end{document}

</format>

