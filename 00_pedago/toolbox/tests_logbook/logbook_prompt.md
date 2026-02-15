
Je fais des appréciations très personnalisées à mes élèves pour chacune de leurs interrogations, et les log dans des fichiers json. Le json en pièce jointe est constituté de 5 clés : 
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
