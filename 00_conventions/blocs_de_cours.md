# Les blocs d'un document de cours

Un document de cours est fait de six types de blocs. Ce fichier dit **lequel utiliser
quand**, et **comment chacun se signale visuellement**. La règle vaut pour le LaTeX
comme pour les Google Docs.

## Le principe

> **Un fond coloré ne sert qu'à dire deux choses : "arrête-toi" ou "écris ici".**
> Tout le reste se signale par un filet, un crochet ou la typographie.

Un encadré plein n'est justifié que si le contenu est **de nature différente** du texte
courant. Un exemple ne l'est pas : il continue le propos, on le lit dans la foulée. Un
avertissement, si : il doit couper la lecture.

Quand tous les blocs ont un fond plein, plus rien ne ressort, et le document devient une
pile de rectangles colorés. C'est arrivé le 2026-09-06 (voir "Historique" en bas).

## Les six blocs

| Bloc | Quand l'utiliser | Traitement |
|---|---|---|
| **Théorie** | la règle et sa justification. Le fil du cours | encadré plein bleu `#E8F4F8`, bordure `#2E75B6`, bandeau de titre |
| **Astuce** | la méthode rapide, le raccourci de calcul mental | encadré plein vert `#D9EAD3`, bordure `#38761D`, bandeau de titre |
| **Attention** | un piège classique, une erreur fréquente d'élève | encadré plein rouge `#FFE5E5`, bordure `#CC0000`, bandeau de titre |
| **À retenir** | la synthèse d'une section : formules, tables, règles à mémoriser | encadré plein jaune `#FFF2CC`, bordure `#E69138`, bandeau de titre |
| **Exemple** | un cas résolu, détaillé étape par étape | **crochet latéral bleu** `#1C4587` + badge "Exemple N". Aucun fond |
| **Exercices** | la série de calculs que l'élève fait lui-même | **bordure fine** `#E69138` à 0,6 pt. Aucun fond. Lettres a. b. c. en `#B45F06` |

### Pourquoi le jaune est réservé à "À retenir"

C'est le seul bloc dont l'élève a besoin **en feuilletant**, la veille d'un contrôle.
Si le jaune ne sert qu'à lui, chercher les taches jaunes dans le document revient à
retrouver toutes les synthèses. Aucune consigne à donner : la mise en page la porte.
Donner au jaune un deuxième usage annulerait ce repère.

### Le crochet des exemples

Le crochet s'ouvre en haut du bloc, longe la marge et se referme en bas : on voit où
l'exemple commence et où il finit, ce qu'une simple barre verticale ne dit pas.

Quand un exemple est coupé par un saut de page, **le crochet reste ouvert du côté de la
coupure** : il descend sans se refermer en bas de page, et ne s'ouvre pas en haut de la
suivante. Le lecteur voit ainsi que l'exemple continue. Cela demande quatre tracés
(bloc entier, début, milieu, fin) que `tcolorbox` choisit automatiquement.

## Implémentation

| Format | Où |
|---|---|
| LaTeX | [`../stylecours.sty`](../stylecours.sty) : `theorie`, `astuce`, `attention`, `aretenir`, `exemple`, `exos`, `exostrois` |
| Google Docs | `gdoc_insert_box.py` dans `~/.claude/scripts/`, et [`google_docs.md`](google_docs.md) section "Encadrés" |

En LaTeX, l'exemple prend **deux arguments** : le badge et le titre.

```latex
\begin{exemple}{Exemple 2}{à quoi ça sert}
  ...
\end{exemple}
```

Les séries d'exercices numérotent **automatiquement** en a. b. c., dans l'ordre de
lecture ligne par ligne, avec remise à zéro à chaque série. Rien à écrire à la main :

```latex
\begin{exos}
\ex{$234 + 99$}  & \ex{$1\,289 - 101$} \\
\ex{$858 - 99$}  & \ex{$2\,658 + 299$} \\
\end{exos}
```

Intérêt de la numérotation : pouvoir dire "on corrige le c." en classe. Sans elle, un
calcul ne peut être désigné que par son contenu.

## Éviter les titres orphelins

Un bloc dont le titre reste seul en bas de page, son contenu passant à la page suivante,
est très visible dès qu'il porte un fond ou un crochet. Chaque bloc réserve donc un
nombre minimal de lignes avant de s'ouvrir (`\needspace`) :

| Bloc | Lignes réservées | Pourquoi |
|---|---|---|
| Exemple | 4,5 | le badge occupe à lui seul une ligne et demie |
| Séries d'exercices | 3 | titre plus deux lignes de calculs |

Ne pas monter plus haut : à cinq lignes, on gagne des sauts de page qui laissent un
tiers de page blanc.

## Les décisions de design, et pourquoi

Chaque choix ci-dessous a été pris contre une alternative défendable. La raison est notée
pour qu'on ne refasse pas le débat, et pour qu'on puisse revenir dessus en connaissance
de cause.

### Pourquoi un crochet pour les exemples, et pas une barre ni un fond

Trois traitements ont été essayés dans l'ordre : barre verticale, fond bleu pâle, crochet.

- La **barre verticale** dit où le bloc commence, mais pas où il finit. Répétée cinq fois
  sur une page, elle produit un effet de rayures qui hache la lecture.
- Le **fond pâle** délimite bien, mais ajoute un sixième aplat à une page qui en comptait
  déjà cinq. C'est ce qui a provoqué le « ce ne sont que des box partout ».
- Le **crochet** délimite début et fin sans aplat, et son ouverture le rend directionnel :
  on lit qu'il enferme quelque chose.

Modèle : les manuels scolaires, qui utilisent ce crochet depuis longtemps pour la même
raison.

### Pourquoi le crochet est bleu et non jaune comme dans le manuel

Le manuel de référence utilise un crochet et un badge jaunes. Ici, le jaune est **déjà
pris** par `À retenir`, et c'est son seul emploi qui lui donne sa valeur (voir plus haut).
Un second usage du jaune ferait perdre le repère de révision. Le bleu de la palette des
exemples est repris à la place.

### Pourquoi les exercices ont une bordure fine et aucun fond

Un fond crème marchait bien isolément, mais il revient une vingtaine de fois dans le
document : ça fait vingt aplats. La bordure fine suffit à dire « zone séparée », et les
pointillés disent déjà « écris ici ». C'est le seul bloc dont la fonction est **de rester
vide**, donc le seul où l'absence de fond ne coûte rien à la lisibilité.

### Pourquoi les exercices sont numérotés a. b. c.

Argument d'usage, pas d'esthétique : sans lettres, un calcul ne peut être désigné à l'oral
que par son contenu (« celui avec 1 289 moins 101 »). Avec elles, on dit « on corrige le
c. ». La numérotation est automatique et suit la lecture **ligne par ligne**, pas colonne
par colonne, parce que c'est le sens de lecture naturel d'un tableau à deux colonnes.

### Pourquoi les schémas sont dessinés en TikZ et pas extraits en image

Les schémas de compensation (les flèches en V avec `+300` / `−1`) existaient en image dans
le cours de 6ème, scannés. Redessinés en TikZ, ils sont nets à toute résolution, prennent
les couleurs de la palette, et se modifient en changeant un paramètre. Les seuls éléments
restés en image sont les deux encadrés du manuel (`×4` et `×5`), qu'on ne peut pas
reproduire sans les recomposer entièrement.

Corollaire appris à l'usage : dans un schéma TikZ, **placer les nœuds les uns par rapport
aux autres**, jamais à des coordonnées fixes. Avec des coordonnées absolues, le schéma se
décale dès que la largeur du texte change d'un exemple à l'autre.

### Pourquoi les étiquettes sont au milieu des flèches

Placées à côté (`above left`, `above right`), elles chevauchaient le résultat sur la flèche
montante. Au milieu (`pos=0.5`) avec un fond blanc qui interrompt le trait, elles sont
toujours lisibles quelle que soit la longueur de la flèche.

### Le schéma de la distributivité : ce qu'on garde de l'image, ce qu'on redessine

Le cours de 6ème (Chapitre 0) illustrait la distributivité par trois images : deux schémas
fléchés (`12 × (2+3)` et `8 × (100+1)`, ce dernier photographié dans un manuel) et un
dessin de six sachets de bonbons contenant chacun 3 schtroumpfs et 4 cocas.

Les deux traitements sont différents parce que les objets sont différents :

- **Les schémas fléchés sont redessinés en TikZ** (`\distrib`). Ce sont des mathématiques,
  donc reproductibles : mêmes flèches, mêmes numéros d'ordre, mais nets, aux couleurs de la
  palette, et paramétrables (`\distrib{8}{100}{1}` suffit à en produire un nouveau). La
  photo de manuel, elle, était floue et grise.
- **Le dessin des sachets reste une image.** Ce n'est pas un schéma mathématique mais une
  illustration : la redessiner en TikZ coûterait très cher pour un résultat moins bon. Elle
  est extraite du PDF du cours de 6ème (`pdfimages`), rognée, et rangée dans `figures/`.

La règle générale : **on redessine ce qui porte le raisonnement, on garde en image ce qui
porte le contexte.**

Deux choix de rendu à l'intérieur de `\distrib` :

- Le facteur répété (`k`) est **coloré et en gras des deux côtés de l'égalité**. C'est lui
  qui voyage ; le voir aux trois endroits est ce qui rend la règle lisible d'un coup d'œil.
- Les numéros d'ordre sont **posés sur les flèches** (`pos=0.40` et `pos=0.5`), pas
  au-dessus des termes. Posés au-dessus, la deuxième flèche passait derrière le premier
  numéro et semblait coupée. Sur la flèche, ils reprennent exactement le langage visuel
  déjà utilisé par `\compensation` : un disque cerclé à fond blanc qui interrompt le trait.

L'oubli du second terme (`k × (a+b) = k × a + b`) étant l'erreur la plus fréquente, la
phrase qui précède le schéma dans le bloc Théorie la nomme explicitement.

### L'espacement après le titre d'un exemple : un seul curseur pour deux cas

Quand un calcul suit **directement** le titre, TeX ouvre un paragraphe vide qui coûte une
ligne entière (13,6 pt). Quand une phrase suit, ce paragraphe n'existe pas. Les deux cas
n'ont donc pas naturellement le même espacement, alors qu'ils devraient se ressembler.

`\par\nointerlineskip` supprime la ligne fantôme : l'air passe de 32 pt à 20 pt dans le
premier cas. Les 3 pt ajoutés ensuite servent au second cas, où le texte se collait au
titre. C'est un **curseur unique** : le baisser resserre le calcul mais colle la phrase,
le monter fait l'inverse. Réglage retenu : 24 pt pour un calcul, 13 pt pour une phrase.

Ne **pas** essayer de descendre plus bas avec un rattrapage négatif : le texte vient alors
chevaucher le badge.

### Pourquoi de vraies lignes vides plutôt que des `\vspace`

Le document contenait 36 `\vspace{0.4em}` et variantes, posés à la main. Ils compensaient
tous la même chose : `\parindent` vaut 0 dans ce repo, et sans `\parskip`, deux paragraphes
consécutifs sont collés et indiscernables. Un `\parskip` défini une fois dans
`stylecours.sty` remplace les 36, et le source devient lisible.

## Historique

- **2026-05-19 — Cinq encadrés suffisent.** Une première proposition à sept encadrés
  colorés a été rejetée pour saturation. Exemples et exercices sont passés en repère
  léger. Voir `pedagogie/erreurs_types.md`.
- **2026-09-06 — Retour au fond plein sur exemples et exercices, puis marche arrière.**
  Les deux blocs sont repassés en fond plein après une comparaison de variantes
  présentées **isolément**. À l'échelle de la page, le résultat était une pile de six
  aplats sans hiérarchie. Le principe en tête de ce fichier a été posé à cette occasion,
  et les exemples ont pris le crochet du manuel.
