Je veux que tu me génères un tableau que je peux directement copier coller depuis l'interface de conversation.

Format attendu :  Les 3 premières colonnes  suivent le format ci-dessous et les suivantes correspondent au numéro d'une question


Les 3 première colonnes doivent être exactement comme suit : 

Index	Prénom	Nom
1	Salomé	Amar
2	Tiziri Lin	Arnaud Zidouni
3	Evan	Baser
4	Aris	Bourbia
5	Eleana	Cognard
6	Ayaan	Corazza
7	Clara	Dandoy
8	Anaëlle	Duvault
9	Sohan	Favereau
10	Myriam	Flichy
11	Max	Gourru
12	Elise	Jendoubi
13	Romane	Lacroix Ferrere
14	Jeanne	Le Pape
15	Mia	Malpeli
16	Sarah	Nejmaoui
17	Evann	Nguendi
18	Harrison	Pick
19	Manon	Remy
20	Lila	Rocher
21	Gabin	Soubies
22	Margaux	Szkorodenszky
23	Karl	Thery Vermersch
24	Juan andres	Zamora Borregales
25	Victor	Zenou

Pour les colonnes relatives aux questions, elles doivent suivre ce format : 
- Ex1Q1 (pour exercice 1 question 1)
- Ex1Q2 (pour exercice 1 question 2)
- Ex2Q1
- Ex2Q2a (pour exercice 2 question 2a)
- Ex2Q2b etc

Voici le devoir

[DEBUT DEVOIR]

\documentclass[answers]{exam}
\usepackage{../../../mypackages}
\usepackage{../../../macros}


\tcbuselibrary{theorems,skins,hooks}

\definecolor{myindbg}{HTML}{DFF5EC}
\definecolor{myindfr}{HTML}{1F6F4A}

\newtcolorbox{Indication}{
  enhanced,
  colback=myindbg,
  colframe=myindfr,
  arc=6mm,
  rounded corners,
  boxrule=0.6mm,
  left=3mm,
  right=3mm,
  top=2mm,
  bottom=2mm
}

\title{Interrogation N°5}
\author{N. Bancel}
\date{3 Février 2026}

% Mise en forme des solutions en bleu
\SolutionEmphasis{\color{blue}}
\renewcommand{\solutiontitle}{\noindent}

\begin{document}

\dsheader{Collège Lycée Suger}{Mathématiques}{Année 2025-2026}{Classe de 6ème}
{\let\newpage\relax\maketitle}
\consignesrendusujet{45 minutes}{0.5}

\section*{Exercice 1 - Cours - Médiatrice et bissectrice (4 points)}

\begin{questions}
  \question[2] \textbf{Médiatrice} Donner la définition précise de la médiatrice d’un segment. Un vocabulaire mathématique est attendu.
    
  \question[2] \textbf{Bissectrice} Donner la définition précise de la bissectrice d’un angle. Un vocabulaire mathématique est attendu.
  \end{questions}

\section*{Exercice 2 - Symétrie axiale - Exercice basique (7 points)}

\begin{questions}
  \question[2] Sur la figure ci-dessous, tracer le symétrique de la figure dessinée à gauche par rapport à la droite $(d)$. Il n'est pas nécessaire ici de mettre de légendes (les tracés sont à faire sur le sujet).
\fig{0.8}{01.png}{}
\end{questions}

\begin{questions}
  \question[5] Sur la figure ci-dessous, tracer le symétrique du cercle $C$ et de rayon $O$ par rapport à la droite $(d1)$, et tracer le symétrique de la droite $(d2)$ par rapport à la droite $(d1)$. \textrr{Vous noterez toutes les légendes nécessaires} (les tracés sont à faire sur le sujet).
\fig{1}{00.jpg}{}
\end{questions}

\section*{Exercice 4 - Axes de symétrie (5 points)}

\begin{questions}
  \question[5] Sans justifier, tracer les axes de symétrie des figures ci-dessous (les tracés sont à faire sur le sujet).
\fig{0.8}{02.jpg}{}
\end{questions}

\section*{Exercice 5 - Déductions (4 points)}

\begin{questions}
  \question[4] Le polygône $DEF$ a pour symétrique par rapport à la droite $(d)$ le polygône $D'E'F'$. $I'$ est le symétrique du point $I$ par rapport à la droite $(d)$. $J \in (DE)$ et $J'$ est le symétrique du point $J$ par rapport à la droite $(d)$. On considérera que les longueurs affichées correspondent à des $cm$, et que $de$ correspond à la longueur du segment $[DE]$,
  que $ef$ correspond à la longueur du segment $[EF]$ 
  et que $df$ correspond à la longueur du segment $[DF]$.
  \fig{0.8}{03.jpg}{}
  \begin{parts}
    \part[1] Que peut-on dire de l'angle $\widehat{E'D'F'}$ ? Justifier.
    \part[1] Que peut-on dire de la longueur $D'F'$ ? Justifier.
    \part[1] Que peut-on dire du point $I'$ par rapport au segment $[E'F']$ ? Justifier.
    \part[1] Que peut-on dire de l'angle $\widehat{E'D'J'}$ ? Justifier.
  \end{parts}

\end{questions}

\end{document}

[FIN DEVOIR]
