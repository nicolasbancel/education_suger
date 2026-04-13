# Macros et environnements disponibles

Raccourcis définis dans `01_2526_6emes_maths/macros.sty` (et `mypackages.sty`). Les utiliser plutôt que de réécrire le code inline. Toujours vérifier la définition actuelle dans `macros.sty` avant de s'appuyer dessus (la macro peut avoir évolué).

## Macros de mise en forme

| Macro | Effet | Exemple |
|---|---|---|
| `\justifier` | Produit `[Justifier]` en gras rouge. À coller devant l'énoncé des questions qui exigent une rédaction. | `\part[0.5] \justifier\ En vous appuyant sur une propriété...` |
| `\textrr{...}` | Texte gras rouge (raccourci pour `\textbf{\textcolor{red}{...}}`). Pour les stratégies et points de vigilance. | `\textrr{Les points H, A, P sont alignés.}` |
| `\textbb{...}` | Texte gras bleu. Défini mais peu utilisé. | |

## Macros de structure de document

| Macro | Effet |
|---|---|
| `\dsheader{col1}{col2}{col3}{col4}` | En-tête standard du DS : ligne 1 = établissement / matière, ligne 2 = année / classe. |
| `\consignes{durée}{coeff}` | Bloc rouge des consignes standard avec rappel sur les questions `[Justifier]`. |
| `\consignesrendusujet{durée}{coeff}` | Variante pour les contrôles rendus sur le sujet. |

Utilisation typique en tête de document :
```latex
\dsheader{Collège Lycée Suger}{Mathématiques}{Année 2025-2026}{Classe de 6ème}
\consignes{1h15}{1.5}
```

## Macro pour les figures

```latex
\fig{largeur}{fichier}{légende}
```

- `largeur` : facteur de `\linewidth` (ex. `0.5`, `0.8`).
- `fichier` : nom de l'image (sans chemin, relative au `.tex`).
- `légende` : peut être vide (`{}`) pour n'afficher aucune légende.

Équivalent à :
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=<largeur>\linewidth]{<fichier>}
  \captionsetup{labelformat=empty,labelsep=none}
  \caption{<légende>}  % ou rien si vide
\end{figure}
```

## Environnement `Indication` (boîte verte)

Boîte `tcolorbox` verte claire bordée vert foncé, coins arrondis. Utilisée pour :
- « Ce qui était attendu »
- Avertissements ciblés avant la solution
- Conseils méthodologiques

```latex
\begin{Indication}
\textbf{Attention : le diamètre fait 6 cm, donc le rayon fait 3 cm.}
\end{Indication}
```

## Environnement `compactparts`

Variante compacte de `parts` (moins d'espace vertical entre les items). Défini localement dans certaines interros :
```latex
\newenvironment{compactparts}
  {\begin{parts}\setlength{\itemsep}{0pt}\setlength{\partopsep}{0pt}}
  {\end{parts}}
```
Utilisation typique : résumer les réponses d'un exercice Vrai/Faux en quelques lignes compactes avant le détail.

## Réglages globaux appliqués aux solutions

Définis en préambule, **ne pas réécrire** :
```latex
\SolutionEmphasis{\color{blue}}
\renewcommand{\solutiontitle}{\noindent}
```
Conséquence : tout contenu entre `\begin{solution}` et `\end{solution}` est automatiquement affiché en bleu, sans titre « Solution: » devant. Donc ne **jamais** ajouter `\color{blue}` manuellement à l'intérieur d'un bloc solution.
