J'ai des élèves de 1ère d'une filière artistique à qui je dois faire un cours sur les matériaux organiques.

Je veux écrire ce cours en LaTex.

Je voudrais que tu organises le cours en plusieurs sections 
- Rappels de 2nde (1 section sur les couches électroniques, les électrons de valence, la formation des ions et des molécules, les doublets liants, règle de l'octet et du duet)
- Puis que tu adresses le programme de 1ère, qui est divisé en plus sections

- Les chaînes carbonées
  - L'atome de carbone (tétravalent, composé organique, chaîne saturée et insaturée, chaînes linéaires, ramifiées, ou cycliques, modélisation des molécules)
  - Modélisation des molécules (formule brut, formule développée, semi développée, formule topologique)

- HYDROCARBURES ET GROUPES CARACTÉRISTIQUES
  - Les alcanes
  - Les alcènes
  - Les composés aromatiques
  - Les groupes caractéristiques

- Les polymères
  - Définition et propriétés
  - Polyaddition et polycondensation

- Plastiques, élastomères et fibre
  - Les plastiques
  - Les élastomères
  - Les adjuvants
  - Température de transition

Liste de contraintes : 

(1) Tu chargeras mon script `mypackages.sty`, qui contient les packages suivants : 

```
\ProvidesPackage{mypackages}[2024/09/02 Custom package collection]

\RequirePackage[english]{babel}

% Set page size and margins
\RequirePackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}

% Useful packages
\RequirePackage{amsmath}
\RequirePackage{tcolorbox}
\RequirePackage{array}
\RequirePackage{booktabs}
\RequirePackage{mathtools}
\RequirePackage{titlesec}
\RequirePackage{pgfplots}
    \pgfplotsset{
    compat=1.11,
  }
\RequirePackage{tikz}
\RequirePackage{tkz-tab}
\RequirePackage{tabularx}
\RequirePackage{fouriernc}
\RequirePackage{hyperref}
\RequirePackage{xcolor}
\RequirePackage{amssymb} % This package provides the \mathbb command
\RequirePackage{graphicx}
% \RequirePackage[colorlinks=true, allcolors=blue]{hyperref}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage[version=4]{mhchem}
\RequirePackage{siunitx}
\RequirePackage{enumitem}
\RequirePackage{pgffor}
\RequirePackage{ifthen}
\RequirePackage{caption}
\RequirePackage{float}     % For using [H] specifier in figure environments
\RequirePackage{xparse}
```

(2) Quand tu donneras une définition ou un exemple d'application, je voudrais que les mettes dans des box {colorbox} avec ces critères

\begin{tcolorbox}[colback=green!10!white, colframe=green!75!black, title=Définition : ]
  Texte
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!10!white, colframe=blue!75!black, title= Application]
Texte
\end{tcolorbox}

(3) Je veux que les listes soient faites sans séparateur / espace entre les bullet points. 

  \begin{itemize}[noitemsep]
    \item Texte
  \end{itemize}

(4) Je voudrais que les tableaux que tu crées aient cette forme là 

\begin{tabular}{p{5cm}p{5cm}p{5cm}}
  \toprule
  {Colonne 1} & {Colonne 2} & {Colonne 3} \\
  \midrule
  Texte 1 & 
  Texte 2 & 
  Texte 3 \\
  \bottomrule
\end{tabular}

(4) Je voudrais que tu me crées du latex paramétrable, avec une variable d'entrée WITH_CORRECTION. Quand WITH_CORRECTION = YES, le document compilé est la version pour le professeur, avec tous les éléments / définitions / exemples remplis. Quand WITH_CORRECTION = NO, le document  compilé est la version élève, avec des trous à la place de certaines définitions, ou mots, ou exemples importants. Les élèves rempliront ces blancs eux-mêmes, afin de mieux s'imprégner du cours.



