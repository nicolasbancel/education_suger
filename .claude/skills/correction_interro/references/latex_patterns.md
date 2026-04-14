# Patterns LaTeX — corrections 6ème

Règles extraites de l'analyse des corrections validées (interro_2 à interro_5). Toutes les observations renvoient à ces fichiers comme source de vérité.

## 1. Environnements de liste

| Environnement | Quand l'utiliser |
|---|---|
| `compactitem` | **Défaut** pour toute liste à puces. Jamais `itemize`. |
| `compactenum` | Listes numérotées (procédures étape par étape, construction géométrique). |
| `parts` | Sous-questions (standard de la classe `exam`). |
| `compactparts` | Variante compacte de `parts`, utilisée pour les résumés de réponses (ex. interro_3 exercice 3 : liste Vrai/Faux condensée). Définie localement via `\newenvironment`. |

## 2. Mise en forme des calculs

### Règle d'or
Un calcul = **un seul** `align*`. Ne JAMAIS écrire `A = 10` sur une ligne puis `A = 11` sur la suivante comme si c'était trois valeurs de A différentes (voir la mise en garde explicite dans `interro_3_correction.tex` lignes 406-416).

### Patron standard
```latex
\begin{align*}
A &= 45 - (16 + 8) + 4 \\
  &= 45 - 24 + 4 && \text{on calcule la parenthèse} \\
  &= 21 + 4     && \text{car } 45 - 24 = 21 \\
  &= 25
\end{align*}
```

- Première ligne : expression complète avec `A &=`.
- Lignes suivantes : `&=` seul au début, alignement vertical.
- Colonne de commentaire à droite via `&& \text{...}` — **utilisée systématiquement** dès qu'une étape non triviale a besoin d'être justifiée (« on calcule la parenthèse », « car … », « on applique la propriété … »).
- Pas de point final après la dernière ligne.

### Variantes
- `align` (avec numérotation) : uniquement pour les démonstrations formelles où les lignes sont référencées.
### `\dfrac` vs `\frac` — règle stricte

- **`\dfrac`** (version display) : uniquement à l'intérieur d'un bloc `\[ ... \]` ou `align*`. Jamais en inline. Rendu gros, illisible quand coincé entre deux lignes de texte.
- **`\frac`** (version adaptative) : autorisé en inline `$...$` **pour une mention unique et isolée** dans une phrase de texte courant (ex. `chaque graduation vaut $\frac{1}{4}$`, `il reste $\frac{1}{3}$ du volume`). Rendu petit, tient naturellement dans la ligne.
- **Interdit dans tous les cas** : enchaîner plusieurs fractions inline (`$\frac{a}{b} = \frac{c}{d} = \frac{e}{f}$`) ou faire une comparaison de fractions inline (`$\frac{a}{b} < \frac{c}{d}$`). Toute relation `=`, `<`, `>`, `\leq`, `\geq`, `\neq` **entre fractions** va obligatoirement en `\[ ... \]`.
- **Nombres entiers** inline : toujours OK (`$56$`, `$32 < 35$`, `$ABC$`).

### Récapitulatif pratique

| Contexte | Forme |
|---|---|
| Calcul enchaîné (plusieurs `=`) | `\[ ... \]` avec `\dfrac` |
| Comparaison de deux fractions | `\[ ... \]` avec `\dfrac` |
| Une seule fraction mentionnée en passant dans une phrase | `$\frac{...}{...}$` inline |
| Nombres entiers, variables, inégalités entre entiers | `$...$` inline |

### Exception unique

Dans un `compactitem` qui présente **plusieurs méthodes côte à côte** (typiquement les deux méthodes de simplification), les items peuvent contenir des `\dfrac` inline chaînés pour préserver le parallèle visuel. C'est la seule exception documentée.

## 3. Emphase et couleurs

| Élément | Usage |
|---|---|
| `\textbf{...}` | Définitions, conclusions finales, points clés, noms de méthodes. Très fréquent. |
| `\textcolor{red}{...}` | Avertissements, consignes critiques, mises en garde méthodologiques. |
| `\textcolor{blue}` | **Ne jamais appliquer à la main** : tout le contenu d'un bloc `\begin{solution}` est déjà bleu grâce à `\SolutionEmphasis{\color{blue}}` défini en préambule. |
| `\textbf{\textcolor{red}{...}}` ou `\textrr{...}` | Combiné gras+rouge pour les points critiques (stratégies, erreurs graves, instructions obligatoires). |
| `\emph{...}` | Rare, pour une nuance ponctuelle. |

### Réponse Vrai/Faux
Toujours commencer la solution par la réponse en gras rouge, AVANT la démonstration :
```latex
\textbf{\textcolor{red}{[VRAI]}}. Les segments $[AG]$ et $[GE]$ ont le même codage, donc ...
```
Terminer par la conclusion réaffirmée en gras : `\textbf{L'affirmation est vraie.}`

## 3bis. Espacement vertical dans les solutions

Laisser **respirer** une solution : insérer un `\\` en fin de phrase entre les blocs logiques, pour aérer le texte. Une solution trop compacte est difficile à lire pour un élève de 6ème.

**À faire** :
```latex
\begin{solution}
  On met au même dénominateur. $7 \times 8 = 56$. \\

  $\dfrac{4}{7} = \dfrac{4 \times 8}{7 \times 8} = \dfrac{32}{56}$ \quad et \quad $\dfrac{5}{8} = \dfrac{5 \times 7}{8 \times 7} = \dfrac{35}{56}$. \\

  Comme $32 < 35$, on a $\dfrac{4}{7} < \dfrac{5}{8}$.
\end{solution}
```

**À éviter** (trop compact) :
```latex
\begin{solution}
  On met au même dénominateur. $7 \times 8 = 56$.

  $\dfrac{4}{7} = \dfrac{4 \times 8}{7 \times 8} = \dfrac{32}{56}$ \quad et \quad $\dfrac{5}{8} = \dfrac{5 \times 7}{8 \times 7} = \dfrac{35}{56}$.

  Comme $32 < 35$, on a $\dfrac{4}{7} < \dfrac{5}{8}$.
\end{solution}
```

Règle pratique : après chaque étape logique de la rédaction (énoncé de la méthode, calcul intermédiaire, conclusion), terminer la ligne par `\\` suivi d'une ligne vide. Ça force un saut de ligne ET un petit espace vertical supplémentaire.

**Exceptions** : pas besoin de `\\` avant/après un bloc display `\[ ... \]` ou `align*` — ces environnements gèrent déjà leur propre espacement vertical.

## 4. Environnement `Indication` (boîte verte)

Défini via `tcolorbox` dans les interros récentes (4, 5). Fond `myindbg` (vert très clair `#DFF5EC`), bordure `myindfr` (vert foncé `#1F6F4A`), coins arrondis.

Contenu typique :
- **« Ce qui était attendu »** suivi d'un `compactitem` (critères de correction).
- **Avertissement ciblé** avant la solution (« Attention : le diamètre fait 6 cm, donc le rayon fait 3 cm »).
- **Rappel méthodologique** (tournures à éviter, réflexes à avoir).

```latex
\begin{Indication}
Ce qui était attendu :
\begin{compactitem}
  \item Voir les 3 points A, B et C.
  \item Que le sommet de l'angle soit bien le point B.
\end{compactitem}
\end{Indication}
```

## 5. Figures

Patron standard :
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.5\linewidth]{nom_image.jpg}
  \captionsetup{labelformat=empty}
  \caption{\label{} Figure 2}
\end{figure}
```
- `[H]` obligatoire (force l'image à rester en place).
- `\captionsetup{labelformat=empty}` supprime la numérotation automatique « Figure 1: ».
- Largeur usuelle : `0.5\linewidth` (petites), `0.6` / `0.8` (moyennes), `1.0` (plein écran).
- Alternative courte : la macro `\fig{largeur}{fichier}{légende}` définie dans `macros.sty` (voir `macros_disponibles.md`).

## 6. Notation mathématique

| Objet | Notation |
|---|---|
| Point | `$A$` (majuscule, italique math) |
| Segment | `$[AB]$` |
| Droite | `$(AB)$` ou `$(d)$` |
| Demi-droite | `$[AB)$` |
| Longueur | `$AB$` (sans crochet) |
| Angle | `$\widehat{ABC}$` |
| Mesure d'angle | `$\widehat{ABC} = 60^\circ$` ou `$60\text{°}$` |

## 7. Nombres et unités

- **Séparateur de milliers** : `\,` (espace fine). Ex. `$80\,431$`, `$100\,000$`.
- **Décimales** : **toujours le point décimal** `$8.5$`. Ne JAMAIS utiliser la virgule française `$8{,}5$`. Si un fichier existant contient `8{,}5`, le remplacer par `8.5` lors de la relecture.
- **Unités** : `~\text{cm}` (tilde = espace insécable, `\text` = romain). Ex. `$AB = 7~\text{cm}$`.
- **Degré** : `$60^\circ$` (préférer) ou `$60\text{°}$`.
- **Espacement horizontal** : `\qquad` entre plusieurs égalités sur la même ligne, `\quad` pour espacement plus court.

## 8. Apostrophes et guillemets

- **Apostrophe** : droite ASCII `'` (jamais `’`, jamais `\textquoteright`).
- **Guillemets** : droits verticaux `"..."` (pas `«»`, pas `` `` '' ``).

## 9. Structure du préambule (ne PAS modifier sauf demande)

```latex
\documentclass[answers]{exam}
\usepackage{../../../mypackages}
\usepackage{../../../macros}

\SolutionEmphasis{\color{blue}}
\renewcommand{\solutiontitle}{\noindent}
```

Les interros récentes ajoutent le support `tcolorbox` pour `Indication`. Cette partie est gérée dans `mypackages.sty` / `macros.sty` ; ne pas la redéfinir localement.
