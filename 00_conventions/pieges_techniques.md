# Pièges techniques

Les erreurs d'outillage rencontrées, avec leur symptôme et la parade. Ce fichier ne parle
pas de pédagogie ni de mise en page (voir `pedagogie/erreurs_types.md` et
`blocs_de_cours.md`) : uniquement des mécanismes qui échouent **silencieusement** ou avec
un message trompeur.

Le point commun de presque toutes ces erreurs : le script se termine sans planter, mais
le travail n'est fait qu'à moitié. D'où la règle générale.

> **Après toute modification par script, compter le résultat.** Un `grep -c` qui confirme
> le nombre attendu coûte deux secondes ; une modification à moitié appliquée se découvre
> trois étapes plus loin, quand on ne sait plus quoi soupçonner.

## Shell

### `echo` avec une chaîne LaTeX en zsh

```bash
echo '\end{document}' >> fichier.tex     # ✗
printf '%s\n' '\end{document}' >> fichier.tex   # ✓
```

zsh interprète les séquences d'échappement : `\e` devient le caractère ESC (U+001B),
invisible dans le fichier. LaTeX plante ensuite sur
`Unicode character ^^[ (U+001B)`, un message qui ne désigne pas la cause.

### `cd` relatif alors que le répertoire courant a déjà changé

Le répertoire de travail **persiste d'un appel de commande à l'autre**. Un
`cd 01_2627_4emes_maths/00_calcul_mental` lancé alors qu'on y est déjà échoue, et avec
`&&` tout ce qui suit est silencieusement sauté — mais les commandes séparées par `;`,
elles, s'exécutent quand même, dans le mauvais répertoire.

Parade : partir d'un chemin absolu (`cd /Users/.../00_calcul_mental`), ou vérifier avec
`pwd` en tête de commande.

### `grep -c` renvoie un code d'échec quand il compte zéro

```bash
grep -c "Overfull" fichier.log && echo suite    # ✗ : s'arrête quand il n'y en a aucun
echo "overfull : $(grep -c 'Overfull' fichier.log)"   # ✓
```

C'est le comportement normal de `grep` (« rien trouvé » = échec), mais il est
contre-intuitif quand on s'en sert pour **compter**. Dans une chaîne `&&`, tout ce qui
suit est silencieusement sauté — précisément dans le cas favorable, celui où il n'y a
aucun défaut.

Parade : mettre le comptage dans une substitution `$( )`, ou chaîner avec `;`.

### VS Code + LaTeX Workshop compile en parallèle

L'extension LaTeX Workshop recompile à chaque sauvegarde du `.tex` et **supprime les
fichiers auxiliaires** derrière elle. Deux conséquences quand on compile aussi de son
côté :

- `latexmk` ne trouve plus son `.fdb_latexmk` et se croit à jour, ou recompile tout ;
- `synctex view` ne trouve plus le `.synctex.gz` et ne renvoie aucune page ;
- et si les deux compilations se chevauchent, le PDF sort **corrompu**
  (`Syntax Error: Kid object (page 1) is wrong type (null)`).

Parade : compiler dans un répertoire de sortie séparé, puis recopier le PDF en place.

```bash
OUT=<un dossier de travail>
mkdir -p $OUT
for i in 1 2 3; do pdflatex -output-directory=$OUT -synctex=1 -interaction=nonstopmode $F.tex > /dev/null 2>&1; done
grep -E "^! " $OUT/$F.log
cp $OUT/$F.pdf ./$F.pdf
```

Les chemins d'inclusion (`../../mypackages`, `figures/…`) restent relatifs au `.tex`,
donc rien d'autre à changer.

## Substitutions et scripts

### `perl -pi -e 's/…/…/'` sans `/g`

Ne remplace que **la première occurrence de chaque ligne**. Rencontré le 2026-09-06 :
trois `\needspace{5\baselineskip}` à corriger, un seul l'a été. Le rendu changeait donc
en partie, ce qui rendait le diagnostic confus.

Parade : `/g`, puis `grep -c` sur le motif pour vérifier qu'il ne reste rien.

### Regex sur des arguments LaTeX contenant des accolades

```
\begin{exemple}{Exemple 1 : $2{,}58 \times 1\,000$}
```

La classe `[^{}]*` s'arrête à la première accolade interne (`{,}`), donc l'argument n'est
pas capturé et l'appel est ignoré **sans erreur**. Le 2026-09-06, 59 appels sur 65 ont
été convertis, et les 6 restants n'ont été vus qu'au comptage.

Parade : pour un argument LaTeX, écrire un petit parseur qui **équilibre les accolades**
(compteur `+1` sur `{`, `-1` sur `}`) plutôt qu'une expression régulière. Et compter le
nombre d'appels avant et après.

### Deux fichiers qui doivent changer ensemble

Le 2026-09-06, un script modifiait `stylecours.sty` (pour passer `\begin{exemple}` à deux
arguments) et un second modifiait le document (pour convertir les appels). Le premier a
échoué sur un `ValueError`, le second a réussi : le document appelait une macro à deux
arguments qui n'en attendait qu'un.

Parade : quand deux fichiers doivent changer ensemble, les modifier dans **un seul
script**, avec tous les `assert` en tête — on vérifie que les deux motifs existent
**avant** d'écrire quoi que ce soit.

### Caractères non latins glissés dans du texte

Un `х` cyrillique s'est retrouvé dans « encхaîne ». Rigoureusement invisible à la
relecture, et LaTeX ne le signale pas toujours.

Parade : après avoir écrit un bloc de texte par script, passer
`grep -nP '[^\x00-\x7FÀ-ſ…]'` ou simplement relire le rendu.

## LaTeX

### Commandes qui n'existent pas dans la configuration du repo

- `\og` et `\fg` (guillemets français) : fournis par **babel french**. Or `mypackages.sty`
  charge `babel` en **english**. Utiliser `\textquotedbl{}`, conformément à la règle des
  guillemets droits de `latex.md`.
- `\up{}` (exposants) : même origine, même absence. `stylecours.sty` en fournit une
  définition de repli.

### Caractères Unicode que la police ne connaît pas

`⚠` (U+26A0) fait échouer la compilation avec `LaTeX Error: Unicode character`. Les
polices utilisées ici ne couvrent pas les pictogrammes. Pas d'emoji dans un document
`pdflatex`.

### Un nom de commande ne peut pas contenir de chiffre

`\newcommand{\exhead1}` échoue avec un message très éloigné de la cause
(`Missing \begin{document}`, `Illegal parameter number`). Utiliser des lettres :
`\exheadA`, `\exheadB`.

### Deux passes de compilation ne suffisent pas toujours

Voir [`workflow_latex.md`](workflow_latex.md) : utiliser `latexmk`, qui relance
`pdflatex` jusqu'à stabilisation.

## Diagnostic visuel

### Un défaut vu à basse résolution peut ne pas exister

Des filets de tableau semblaient manquer entre certaines lignes à 150 dpi. À 400 dpi, ils
étaient tous là : c'était de l'anticrénelage.

Parade : avant de signaler un problème de rendu, le confirmer à 400 dpi avec un cadrage
serré (`pdftoppm -r 400 -x … -y … -W … -H …`).

### Mesurer plutôt que deviner

Un espacement jugé « trop gros » a d'abord été attribué à `\abovedisplayskip`, puis à
`\parskip`. Les deux ont été réduits sans effet visible. La cause réelle — un paragraphe
vide de 13,6 pt — n'est apparue qu'en compilant un fichier de test comparant quatre
variantes côte à côte.

Parade : quand deux corrections successives ne changent rien, **arrêter de corriger et
construire un fichier de mesure** : le même contenu, plusieurs variantes, une seule page,
et on regarde.
