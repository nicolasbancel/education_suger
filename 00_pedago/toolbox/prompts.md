# Retranscription d'un texte du livre

Retranscris moi le texte suivant en LaTex, en suivant les contraintes suivantes
- Les bullet points doivent être en format `\begin{compactitem} \end{compactitem}`
- Les apostrophes doivent être des ' et pas des ’
- Quand tu écris une formule mathématique sur une même ligne, je veux que tu utilises la notation $xxx$, plutôt que \(xxx\)

# Appréciations

## 1ère intéraction

Les fichiers ci-joints
- ecoledirecte_1er_trimestre : recense les appréciations et moyenne pour chaque élève au 1er trimestre (je veux que tu t'en serves pour évaluer l'évolution par rapport à ce que j'avais déjà relevé au trimestre précédent)
- logbook_2eme_trimestre : est un brouillon d'évaluations pour ce trimestre pour chacun de mes élèves.

A partir des fichiers suivants qui donnent des indications d'appréciations que tu pourrais faire pour chaque élève, je veux que tu rédiges 2 appréciations pour {First Name} dans laquelle tu ajoutes le fait que 

- Comportement / concentration inconstante
- Continuer sur la participation
- Non écoute de mes notes vocales sur LogBook, ce n'est pas acceptable.

- La première appréciation doit faire 400 caractères et correspond à "Appréciations et Conseils".
- La seconde appréciations doit faire 200 caractères et correspond à "Elements travaillés"


## 2ème intéraction

Fais la même chose pour xxxx et pour xxx, je veux que tu ajoutes les éléments suivants : 




# Retranscription en questions

Retranscris moi en LaTex le texte ci-dessous en utilisant le format 

\begin{questions}
  \question[2] 
  \begin{parts}
    \part[1]
    \part[1] 
  \end{parts}
  \question[1] 
\end{questions}

pour les questions. Tu peux associer un nombre arbitraires de points à chaque question. 

Pour les équations chimiques, je veux que tu utilises le module \ce{}

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

Optionnel : 
Tu mettras l'énoncé dans une colorbox, en mettant en gras le numéro de l'exercice. Et je veux ensuite que tu insères les réponses aux questions, en étant pédagogue, pour que mes élèves de 1ère comprennent les étapes du raisonnement

Je vais te passer une image qui correspond à un énoncé d'exercice. Je veux que tu restranscrives cet énoncé en latex 


Contraintes LaTex
- Je veux que pour dessiner des vecteurs, tu utilises la fonction $\overrightarrow{DF}$
- Pour définir un repère orthonormé, tu utilises cette notation : $\left(O\mathpunct{} ; \ \overrightarrow{OA}\mathpunct{}, \ \overrightarrow{OB}\mathpunct{}, \ \overrightarrow{OE}\right)$
- Pour les bullet points, je veux que tu utilises \begin{compactenum}
- pour les apostrophes, que tu fasses des ' au lieu de ’
- ne retranscris pas l'énoncé
- n'ajoute pas de \vspace{} entre 2 subsections


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

Je veux que tu intercales la réponse entre des environnements LaTex \begin{solution} \end{solution} juste après la \question{}. Dans l'environnement solution, ne mets aucune couleur, j'ai déjà configuré l'environnement pour que la réponse soit en couleur.

Contraintes : 
- Tu utiliseras \begin{itemize}[noitemsep] quand tu voudras faire des bullet points
- Mets des phrases en couleur (bleu ou rouge) quand elles sont très importantes
- Je veux que tu utilises les mêmes librairies que dans l'énoncé : \ce ou \chemfig
- Suis les mêmes libraires, façons d'écrire (les vecteurs, formules chimiques etc) que dans l'énoncé
- mes élèves ne sont pas toujours à l'aise avec les calculs donc je veux que tu décomposes tous les calculs
- Les formules mathématiques centrées doivent utiliser [\ xxx \] tandis que au sein d'une même ligne, je veux que tu utilises $ xxx $ et pas (\ xxx \).
- Quand plusieurs équations se suivent, utilise le mode \begin{align*} \end{align*}
- Je veux aussi que tu décomposes un raisonnement scientifique en plusieurs étapes : formules, conversions, application numérique. Ne note pas les unités dans l'application numérique.
- Ecris les accents normalement : "périodique" plutôt que "p\'eriodique". "être déduit" plutôt que "\^etre d\'eduit".


Contraintes sur le programme. Mes élèves ne connaissent pas
- les démonstrations par récurrence
- les calculs de déterminants pour les fonctions

Voici un exemple d'un exercice bien corrigé : 

```latex
\begin{questions}
  \question[1] Estimer en grammes la masse d'un soldat de plomb.
  \begin{solution}
  
    On commence par calculer la masse d'un soldat en utilisant la masse totale pour 25 soldats.

    \textcolor{blue}{\textbf{Formule utilisée :}}
    \[
    m_{\text{soldat}} = \frac{m_{\text{total}}}{N_{\text{soldats}}}
    \]
    où
    \begin{addmargin}[4em]{1em}
      \begin{compactitem}
          \item [$N_{\text{soldats}}$] représente le nombre de soldats
          \item [$m_{\text{total}}$] représente la masse totale des soldats
          \item [$m_{\text{soldat}}$] représente la  masse d'un soldat
      \end{compactitem}
      \end{addmargin}

  On va vouloir exprimer la masse d'un soldat en grammes, donc on fait d'emblée la conversion nécessaire : $m_{\text{total}} = \SI{1.4}{kg} = \SI{1400}{g}$

  \textbf{Application numérique}
    \begin{align*}
      m_{\text{soldat}} &= \frac{1400}{25} \\
      m_{\text{soldat}} &= 56
    \end{align*}

    \textbf{La masse d'un soldat est donc de 56 g.}
  \end{solution}
  \question[1] Calculer la masse volumique du matériau composant les soldats.
  \begin{solution}
    La masse volumique \( \rho \) est définie par la formule suivante :
    \[
    \rho = \frac{m}{V}
    \]

    Pour un soldat, la masse est \( 56 \ \text{g} \) et le volume est \( 5 \ \text{cm}^3 \). Il suffit d'appliquer la formule du dessus pour déterminer la masse volumique du matériau qui le compose.

    \textbf{Application numérique}
    \begin{align*}
      \rho &= \frac{56}{5} \\
      \rho &= 11.2
    \end{align*}

  \textbf{La masse volumique des soldats est donc de $\SI{11.2}{g/cm^3}$}
  \end{solution}

  \question[0.5] En déduire le matériau utilisé pour fabriquer les soldats.
  \begin{solution}
    \begin{itemize}[noitemsep]
      \item La masse volumique du plomb est \( 11.3 \ \text{g/cm}^3 \).
      \item La masse volumique du fer est \( 7.7 \ \text{g/cm}^3 \).
    \end{itemize}

    \textcolor{blue}{\textbf{La masse volumique mesurée (11.2 g/cm$^3$) est très proche de celle du plomb (11.3 g/cm$^3$). On peut donc en conclure que les soldats sont donc fabriqués en plomb.}} 
  \end{solution}
\end{questions}
```


L'image à laquelle fait référence l'exercice de géométrie dans l'espace est en pièce jointe

## Correction automatique

Je vais te passer un contrôle de Mathématiques


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

