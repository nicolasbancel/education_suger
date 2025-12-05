```latex
      %{2} & {\ce{He}} & {\trou{v}{1}{Hello}} \\
        %{2} & {\ce{He}} & \trou{v}{1}{(\(1s)^2\)} \\
    % {2} & {\ce{He}} & {\trou{v}{1}{(1s)^2}} \\
    % {2} & {\ce{He}} & \trou{v}{1}{hello} \\
    %{10} & {\ce{Ne}} & {\trou{v}{1}{\((1s)^2(2s)^2(2p)^6\)}} \\
    %{18} & {\ce{Ar}} & {\trou{v}{1}{\((1s)^2(2s)^2(2p)^6(3s)^2(3p)^6\)}} \\

        %\hlgray{$#3$}
```


\begin{tcolorbox}[colback=green!10!white, colframe=green!75!black, title=Définitions : ]
  La famille des gaz nobles est la famille des éléments chimiques dont la couche de valence est \textbf{saturée} \par
  \vspace{1em}
  \begin{tabular}{l l l}
    \toprule
    {Numéro atomique} & {Element} & {Configuration électronique} \\
    \midrule
    {2} & {Test} & {Test} \\
    \bottomrule
  \end{tabular}

\end{tcolorbox}








Content of 

\documentclass{article}
\usepackage{../../mypackages}
\usepackage{../../macros}

% Variable de correction


% Variable de correction
% \newif\ifWITHCORRECTION
% \WITHCORRECTIONtrue % Mettre \WITHCORRECTIONfalse pour la version élève

% Commandes pour masquer du texte en fonction de la version
%\newcommand{\corrige}[2]{\ifWITHCORRECTION #1 \else \underline{\hspace{#2}} \fi}



\def\WITH_CORRECTION{YES}

\title{Chapitre 2 - Les Matériaux Organiques}
\author{N. Bancel}
\date{Septembre 2024}



\begin{document}

\maketitle

\begin{comment}

% Rappels de 2nde
\section{Rappels de 2nde}
\subsection{Couches électroniques et électrons de valence}
\begin{tcolorbox}[colback=green!10!white, colframe=green!75!black, title=Définitions : ]
  Les électrons se répartissent autour du noyau atomique selon des couches électroniques et des sous-couches. \par 
  \vspace{1em}
  Les \textbf{couches électroniques} sont notées \(n = 1, 2, 3\) etc \par 
  Chaque couche électronique est divisée en \textbf{sous-couches} qui sont notées par les lettres \(s\), \(p\), etc.
  \begin{itemize}[noitemsep]
    \item La sous-couche \(s\) peut contenir jusqu'à \trou{h}{10}{2 électrons.}
    \item La sous-couche \(p\) peut contenir jusqu'à \trou{h}{10}{6 électrons.}
  \end{itemize}

  Dans la configuration électronique à l'état fondamental d'un atome de numéro atomique \trou{h}{60}{inférieur ou égal à 18, les électrons \textit{ns} et \textit{np} associés à la plus grande valeur de \textit{n} sont appelés \textbf{électrons de valence}}
  
  Seuls les électrons de la couche externe (électrons de valence) participent aux liaisons entres atomes dans les molécules, ou à la formation d’ions. 
  
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!10!white, colframe=blue!75!black, title=Application : Structure électronique]
  Exemple de l'atome d'oxygène (O) : Numéro atomique : \(Z = 8\) \\
  Sa configuration électronique est : \trou{h}{10}{\(1s$^2$ 2s$^2$ 2p$^4$\)}. \\
  Cela signifie :
  \begin{itemize}[noitemsep]
    \item \trou{h}{10}{2} électrons dans la première couche (1s$^2$)
    \item \trou{h}{10}{2} électrons dans la sous-couche s de la deuxième couche (2s$^2$)
    \item \trou{h}{10}{4} électrons dans la sous-couche p de la deuxième couche (2p$^4$)
  \end{itemize}
  Il possède donc \trou{h}{20}{6 électrons de valence (2s$^2$ 2p$^4$).}
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!10!white, colframe=blue!75!black, title=Application : Autres configurations électroniques]
  \begin{itemize}[noitemsep]
    \item Hydrogène (H) (Z = 1) : \trou{h}{10}{1s$^1$}
    \item Carbone (C) (Z = 6) : \trou{h}{10}{1s$^2$ 2s$^2$ 2p$^2$}
    \item Sodium (Na) (Z = 11) : \trou{h}{10}{1s$^2$ 2s$^2$ 2p$^6$ 3s$^1$}
  \end{itemize}
\end{tcolorbox}

\subsection{Stabilité des gaz nobles}

\subsection{Formation des ions et des molécules}
\begin{tcolorbox}[colback=green!10!white, colframe=green!75!black, title=Définition : ]
  Un ion est un atome ou une molécule qui a gagné ou perdu des électrons, devenant ainsi chargé positivement ou négativement.
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!10!white, colframe=blue!75!black, title=Exemple : Ions courants]
  \begin{itemize}[noitemsep]
    \item L'ion sodium (Na$^+$) : Perd un électron pour atteindre une configuration stable (1s$^2$ 2s$^2$ 2p$^6$).
    \item L'ion chlorure (Cl$^-$) : Gagne un électron pour compléter sa couche externe (1s$^2$ 2s$^2$ 2p$^6$ 3s$^2$ 3p$^6$).
  \end{itemize}
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!10!white, colframe=blue!75!black, title=Application : Règle de l'octet et du duet]
  La règle de l'octet stipule que les atomes cherchent à obtenir une couche externe remplie de 8 électrons (ou 2 électrons pour les plus petits éléments comme l'hydrogène).
  \begin{itemize}[noitemsep]
    \item Exemple : Le fluor (F) gagne 1 électron pour atteindre 8 électrons sur sa dernière couche et forme un ion F$^-$.
    \item L'hydrogène (H) suit la règle du duet et cherche à obtenir 2 électrons sur sa couche externe en formant une liaison.
  \end{itemize}
\end{tcolorbox}

\subsection{Le tableau périodique de Mendeleïev}
\begin{tcolorbox}[colback=green!10!white, colframe=green!75!black, title=Définition : ]
  Le tableau périodique classe les éléments chimiques en fonction de leur numéro atomique et de leurs propriétés chimiques similaires.
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!10!white, colframe=blue!75!black, title=Application : Position des éléments]
  \begin{itemize}[noitemsep]
    \item Les éléments dans une même colonne (groupe) ont des propriétés chimiques similaires et le même nombre d'électrons de valence.
    \item Exemple : Les éléments du groupe 1, comme le sodium (Na) et le potassium (K), ont un seul électron de valence.
  \end{itemize}
\end{tcolorbox}

% Programme de 1ère
\section{Les Matériaux Organiques}

\subsection{Les chaînes carbonées}
\subsubsection{L'atome de carbone}
\begin{itemize}[noitemsep]
    \item L'atome de carbone est tétravalent.
    \item Les composés organiques contiennent du carbone.
    \item Chaînes saturées, insaturées, linéaires, ramifiées ou cycliques.
\end{itemize}

\subsubsection{Modélisation des molécules}
\begin{itemize}[noitemsep]
    \item Formule brute : CH$_4$
    \item Formule développée : "H--C--H"
\end{itemize}

\subsection{Hydrocarbures et Groupes Caractéristiques}
\subsubsection{Les alcanes}
\begin{tcolorbox}[colback=green!10!white, colframe=green!75!black, title=Définition : ]
  Les alcanes sont des hydrocarbures saturés ne comportant que des liaisons simples entre les atomes de carbone.
\end{tcolorbox}

% Exemple de tableau
\subsubsection{Groupes caractéristiques}
\begin{tabular}{p{5cm}p{5cm}p{5cm}}
  \toprule
  Groupe fonctionnel & Exemple de molécule & Formule \\
  \midrule
  Alcool & Éthanol & \ce{C2H5OH} \\
  Aldéhyde & Formaldéhyde & \ce{CH2O} \\
  \bottomrule
\end{tabular}

\section{Les Polymères}
\subsection{Définition et propriétés}
\begin{tcolorbox}[colback=green!10!white, colframe=green!75!black, title=Définition : ]
  Un polymère est une macromolécule formée par la répétition d'unités monomères.
\end{tcolorbox}

% Plastiques, élastomères, et fibres
\section{Plastiques, élastomères et fibres}
\subsection{Les plastiques}
\begin{itemize}[noitemsep]
    \item Les plastiques sont des polymères synthétiques
\end{itemize}

\end{comment}

\end{document}
