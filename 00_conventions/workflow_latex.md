# Workflow LaTeX

Comment on modifie, vérifie et montre un document LaTeX. Ce fichier décrit la
**procédure de travail** ; les conventions de contenu sont dans [`latex.md`](latex.md),
le style visuel dans [`../stylecours.sty`](../stylecours.sty).

## La règle : ne jamais annoncer un correctif sans l'avoir vu

Un document LaTeX qui **compile** n'est pas un document qui **rend bien**. Une pastille
peut compiler parfaitement et occuper trois fois trop de place ; un tableau peut compiler
et déborder de la page. La seule preuve qu'un correctif fonctionne est visuelle.

Après toute modification d'un `.tex` ou d'un `.sty` (correction de bug, changement de
style, ajout de contenu), la séquence est **obligatoire et dans cet ordre** :

1. **Compiler deux fois** avec `-synctex=1`
2. **Vérifier le log** : zéro erreur, zéro référence indéfinie, zéro débordement
3. **Localiser la page** qui correspond à la ligne modifiée, avec `synctex`
4. **Ouvrir le PDF à cette page** pour l'utilisateur
5. **Regarder le rendu** (image de la page) avant d'annoncer que c'est corrigé

L'étape 4 n'est pas un confort : elle évite à l'utilisateur de chercher lui-même, dans un
document de 30 pages, l'endroit dont on parle.

## La commande complète

```bash
cd <dossier du .tex>
FILE=<nom du fichier sans extension>
LIGNE=<numéro de la ligne modifiée dans le .tex>

# 1. Compilation : latexmk relance pdflatex autant de fois qu'il le faut
latexmk -pdf -synctex=1 -interaction=nonstopmode $FILE.tex

# 2. Contrôles : les trois doivent être vides ou valoir 0
grep -E "^! " $FILE.log
grep -ci "undefined" $FILE.log
grep -c "Overfull \\\\hbox" $FILE.log

# 3. De la ligne du source à la page du PDF
PAGE=$(synctex view -i $LIGNE:1:$FILE.tex -o $FILE.pdf | grep -m1 '^Page:' | cut -d: -f2)

# 4. Ouverture à la bonne page
open -a "Google Chrome" "file://$PWD/$FILE.pdf#page=$PAGE"
```

**Pourquoi Chrome et pas Aperçu** : Aperçu ne sait pas ouvrir un PDF à une page donnée
depuis la ligne de commande, et l'y forcer demanderait de simuler des frappes clavier
(autorisation d'accessibilité, fragile). Chrome comprend `#page=N` nativement, sans
autorisation. Si le document est déjà ouvert dans Aperçu, il se rechargera tout seul à la
compilation suivante, donc les deux peuvent cohabiter.

**Pourquoi `-synctex=1`** : cette option produit un fichier `.synctex.gz` qui fait
correspondre chaque ligne du source à une position dans le PDF. Sans elle, `synctex view`
ne peut rien dire. Le `.synctex.gz` est ignoré par git (voir `.gitignore`).

## Contrôle visuel avant d'annoncer

En plus d'ouvrir le PDF pour l'utilisateur, produire une image de la page et **la
regarder** :

```bash
# Vue d'ensemble d'une page : 150 dpi suffit pour juger la mise en page
pdftoppm -png -r 150 -f $PAGE -l $PAGE $FILE.pdf /tmp/apercu

# Détail (un filet de tableau, un espacement) : monter en résolution et cadrer
pdftoppm -png -r 400 -f $PAGE -l $PAGE -x 900 -y 1450 -W 1600 -H 700 $FILE.pdf /tmp/zoom
```

Une vérification à basse résolution peut faire croire à un défaut qui n'existe pas
(l'anticrénelage fait disparaître les filets fins). Avant de signaler un problème de
rendu, **le confirmer à 400 dpi**.

## Compiler avec `latexmk`, pas avec `pdflatex` à la main

La première passe écrit le sommaire et les références dans le `.aux` ; la seconde les
lit. Après une seule passe, le sommaire est vide ou périmé et les `\ref` affichent `??`.

**Mais deux passes ne suffisent pas toujours.** Quand la structure du document change
beaucoup (blocs ajoutés, hauteur des encadrés modifiée, `\needspace` qui déplace des
blocs), la pagination de la passe 2 diffère encore de celle de la passe 1, et il en faut
une troisième, parfois une quatrième. Constaté le 2026-09-06 sur le document de calcul
mental : le nombre de pages oscillait entre 30 et 31 et deux références restaient
indéfinies après deux passes.

`latexmk -pdf` relance `pdflatex` **autant de fois que nécessaire**, jusqu'à ce que le
`.aux` soit stable, puis s'arrête. C'est la commande à utiliser par défaut. En bonus, il
ne recompile rien si le source n'a pas changé.

Symptôme à connaître : si `grep -ci "undefined"` ne retombe pas à 0 après compilation,
ce n'est pas forcément un `\label` manquant — c'est souvent une passe de trop qui
manque.

## Ne jamais écraser les modifications de l'utilisateur

L'utilisateur édite les `.tex` de son côté, entre deux échanges. Par défaut, procéder par
**modifications chirurgicales** : remplacer une chaîne précise, insérer un bloc à un
endroit identifié. Ne jamais réécrire une section entière ou régénérer un fichier complet,
sauf demande explicite.

Si une différence inattendue apparaît dans le fichier (un passage disparu, une formulation
changée), c'est **presque toujours une modification volontaire de l'utilisateur** : la
signaler, et ne pas la restaurer.

## Nettoyage

Les fichiers `.aux`, `.log`, `.out`, `.synctex.gz` sont ignorés par git. Le `.toc` ne
l'est pas encore. Ne pas les supprimer entre deux compilations : le `.aux` et le `.toc`
portent le sommaire et les références d'une passe à l'autre.
