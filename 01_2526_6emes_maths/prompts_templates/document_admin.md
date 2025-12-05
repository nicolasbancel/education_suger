

## Template

### Tâche

Génère moi en LaTex un document qui résume le barème que j'attends pour les cahiers et lutins de mes 6ème

Le format doit être un tableau de 4 colonnes 

- Catégorie
- Critère évalué
- Description 
- Points

### Contraintes

- Il faut que le tableau puisse dépasser d'une page sur l'autre et se continuer à la page suivante
- Le texte d'une colonne doit être wrappé.
- La colonne Description doit être avoir suffisament de place

### Input / données

- Voici le tableau que tu dois mettre en forme. Mets bien de l'espace, il faut que les lignes du tableau respirent
- Tu peux colorer / remplir en bleu ciel le header
- Et ajoute une ligne Total pour le nombre de points à la fin, dont la couleur de remplissage est le vert


Catégorie	Critère évalué	Points
Cahier d’exercices	Titres des exercices présents et soignés (+ utilisation de couleur)	2
	Ordres de grandeurs notés	1
	Corrections notées (ou rattrapées en cas d'absence)	3
Lutin	Feuilles rangées dans l’ordre	1
	Chaque feuille imprimée dans un feuillet transparent (1 page par feuillet)	1
	Interrogations + calcul mental faciles à retrouver	2
	Cours complet (rien de manquant)	2
	Leçons, phrases, définitions recopiées correctement (traits à la règle + compas etc)	2
Général	Organisation générale (titres soulignés, utilisation de couleurs etc)	2
	Écriture soignée et lisible	1
	Peu ou pas de ratures	1
	Pas de feuilles volantes	1
	Présence de prénom / nom // Identification facile du lutin	1
	Total	20

### Valeurs des variables

Dans le template LaTex ci-dessous, tu remplaceras les variables par ces valeurs : 
- [TITRE] : Barème de notation des cahiers
- [DATE] : 2 Décembre 2025
- [SOUS-TITRE] : Liste des attendus pour la tenue du cahier d'exercices et du lutin

### Contraintes LaTex

Voici l'entête du document LaTex


\documentclass[answers]{exam}
\usepackage{../../../mypackages}
\usepackage{../../../macros}

\title{[TITRE]}
\author{N. Bancel}
\date{[DATE]}

% Mise en forme des solutions en bleu
\SolutionEmphasis{\color{blue}}
\renewcommand{\solutiontitle}{\noindent}

\begin{document}

\textbf{Collège Lycée Suger}
\hfill
\textbf{Mathématiques} \\

\textbf{Année 2025-2026}
\hfill
\textbf{Classe de 6ème} \par

{\let\newpage\relax\maketitle}

\begin{center}
  \textbf{\textcolor{blue}{[SOUS-TITRE]}}
\end{center}

\end{document}

