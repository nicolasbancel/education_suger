# Cheat Sheet - LaTex


## Maths - Suites

```latex
% Suite définie par récurrence

  \[
  \left\{
  \begin{array}{l}
      U_{n+1} = U_n + 3 \\
      U_0 = 2
  \end{array}
  \right.
  \]
```

## Maths - Repères de l'espace

```latex 
% Coordonnées
$A(1; 0; 0)$

% Repère
$\left(O\mathpunct{} ; \ \overrightarrow{OA}\mathpunct{}, \ \overrightarrow{OB}\mathpunct{}, \ \overrightarrow{OE}\right)$

% Vecteurs et opérations sur les vecteurs

 \[
      \begin{pmatrix}
        x_{AE} \\
        y_{AE} \\ 
        z_{AE}
      \end{pmatrix}
      = 
      \begin{pmatrix}
        x_{E} - x_{A} \\
        y_{E} - y_{A} \\ 
        z_{E} - z_{A}
      \end{pmatrix}
    \]
    


## Formules + Légendes des formules

```latex
\begin{tcolorbox}[colback=gray!10!white, colframe=gray, title=Document 4 - La vitesse]
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
  \end{tcolorbox}
```

## Vecteurs et repères orthonormés

```
$\left(O\mathpunct{} ; \ \overrightarrow{OA}\mathpunct{}, \ \overrightarrow{OB}\mathpunct{}, \ \overrightarrow{OE}\right)$ est un repère orthonormal de l'espace.
```

```latex

% Repère A, i, j, k 
$\left(A\mathpunct{} ; \ \vec{\imath}\mathpunct{}, \ \vec{\jmath}\mathpunct{}, \ \vec{k}\right)$

% Equivalences de vecteurs
\[
  \vec{\imath} = \frac{1}{8} \overrightarrow{AB} ; 
  \vec{\jmath} = \frac{1}{8} \overrightarrow{AD} ; 
  \vec{k} = \frac{1}{8} \overrightarrow{AE} ;
\]


```


```latex
% Vecteurs
  \[
  \begin{pmatrix}
    x_{AE} \\
    y_{AE} \\ 
    z_{AE}
  \end{pmatrix}
  = 
  \begin{pmatrix}
    x_{E} - x_{A} \\
    y_{E} - y_{A} \\ 
    z_{E} - z_{A}
  \end{pmatrix}
\]

% Normes
 \[
  AE = \sqrt{(x_A - x_E)^2 + (y_A - y_E)^2 + (z_A - z_E)^2}
  
% Suite d'équations / de calculs de vecteurs

\begin{align*}
  \overrightarrow{AE} \cdot \overrightarrow{DF} &= -1 \times 0 + 0 \times 1 + 1 \times -1 \\
  \overrightarrow{AE} \cdot \overrightarrow{DF} &= -1
\end{align*}


```

## Alignement in equations

```latex
% align* will not number the equations
  \begin{align}
    AE &= \sqrt{(1-0)^2 + (0 - 0)^2 + (0 - (-1))^2} \\
    AE &= \sqrt{(1)^2 + (0)^2 + (1)^2} \\
    AE &= \sqrt{2} \\
  \end{align}
```


## Nombres et unités




## Boxes

```latex
\begin{tcolorbox}[colback=green!10!white, colframe=green!75!black, title=Définition : xxx]
  Voici la définition de blablabla
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!10!white, colframe=blue!75!black, title=Exemples - Application]
  Voici un exemple de blablabla
\end{tcolorbox}
```

## Figures

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.3\linewidth]{title.jpg}
  \captionsetup{labelformat=empty}
  \caption{\label{} Blablabla}
\end{figure}
```

## Conversions

```latex
% with units
\SI{5.0e4}{kg}
% without units
\num{1e-10}
```

## Tables

Way to control automatically the width 

\begin{tabular}{SS}
  \toprule
  {Constituant} & {Masse (en \si{kg})} \\
  \midrule
  {Electron} & {\(9.1 \times 10^{-31}\)} \\
  {Nucléon (Proton et Neutron)} & {\(1.7 \times 10^{-27}\)} \\
  \bottomrule
\end{tabular}



\chemfig{H_3C-CH_2-CH_2-COOH}

\chemfig{[:45]--[:-45]--[:-45]-(-[2]H)-[:-45]-(-[2]CH_3)}
\chemfig{[:45]--[:-45]--[:-45]--[:-45]--[:-45]--[:-45]--[:-45]--[:-45]--[:-45]}
