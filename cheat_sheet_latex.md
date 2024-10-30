# Cheat Sheet - LaTex


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
