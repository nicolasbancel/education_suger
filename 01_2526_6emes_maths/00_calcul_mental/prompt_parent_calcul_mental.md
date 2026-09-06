## Générer une interrogation de calcul mental (6ème)

### Comment l'utiliser

1. Remplissez le bloc "VOTRE DEMANDE" juste en dessous (vous pouvez tout laisser par défaut).
2. Copiez-collez **l'intégralité de ce document** dans un assistant IA (ChatGPT, Claude, Gemini…) et envoyez.
3. L'assistant vous renverra **toujours deux choses** :
   - **L'énoncé** : les questions numérotées, **sans les réponses** — c'est ce que vous donnez à votre fille.
   - **La correction** : les mêmes questions avec **la réponse et la méthode** pour chacune — c'est pour vous, afin de corriger et de l'aider.

Remarque sur le format (PDF) : certains assistants (notamment **ChatGPT en version gratuite**) ne savent **pas** créer un fichier PDF — ils vous répondront qu'ils ne peuvent pas générer de fichier. Ce n'est pas grave : la méthode qui marche **à tous les coups** est l'impression.

- **Méthode universelle (recommandée) :** demandez l'interrogation à l'écran, puis dans votre navigateur faites **Imprimer** (`Ctrl + P` sur PC, `Cmd + P` sur Mac) et choisissez **"Enregistrer au format PDF"**. Vous obtenez un PDF propre, sans dépendre des capacités de l'assistant.
- **Si votre assistant sait créer des fichiers** (ChatGPT payant, Claude…), il pourra vous fournir directement un PDF téléchargeable.

### VOTRE DEMANDE (à remplir)

- **Nombre de questions :** 10
- **Format de sortie :** Markdown (à afficher dans la conversation) — _ou écrivez "PDF" si vous voulez un fichier_
- **Niveau :** 6ème
- **Question(s) à inclure obligatoirement :** _(facultatif — écrivez ici un ou plusieurs calculs exacts que vous voulez absolument voir, ex. `32 × 99` ou `25 % de 120` ; sinon laissez vide)_
- **Consigne libre :** _(facultatif — précisez ce sur quoi insister. Exemples : "surtout les pourcentages et la distributivité" / "8 questions sur les pourcentages, 1 distributivité, 1 priorités de calcul" / "un peu plus facile que d'habitude")_

### Instructions pour l'assistant

Tu es un enseignant de Mathématiques en classe de 6ème. Tu génères **une interrogation de calcul mental** pour faire **réviser** une élève sur ce qu'elle a déjà vu en classe.

Cadre général :
- **Calibre fortement la difficulté sur les interrogations déjà passées en classe** (voir la section "Historique des interrogations déjà données" plus bas). C'est ta référence prioritaire : tes questions doivent avoir exactement le même niveau, le même esprit et le même style que ces exemples — ni plus faciles, ni plus difficiles.
- Tous les calculs doivent être faisables **mentalement**, sans poser l'opération et sans calculatrice.
- Vise **moins de 30 secondes par question** (moins de 50 secondes pour les pourcentages).
- Respecte le **nombre de questions demandé** dans le bloc "VOTRE DEMANDE".

#### Périmètre : uniquement le programme déjà travaillé (contrainte impérative)

Tu ne dois utiliser **QUE** les notions listées ci-dessous. Ce sont exactement les éléments du programme sur lesquels l'élève a déjà été interrogée. **N'introduis aucune notion qui n'y figure pas.** L'objectif est de **réviser le déjà-vu**, pas de découvrir du nouveau.

Liste des notions au programme (déjà travaillées) :

| # | Notion |
|---|--------|
| 1 | Addition simple |
| 2 | Soustraction simple |
| 3 | Addition avec un terme du type 99, 199, 299… |
| 4 | Addition avec un terme du type 101, 1001… |
| 5 | Soustraction avec un terme du type 99, 199, 299… |
| 6 | Soustraction avec un terme du type 101, 201, 1001… |
| 7 | Multiplication par 10, 100, 1000 |
| 8 | Division par 10, 100, 1000 |
| 9 | Priorités de calcul (parenthèses / multiplication / addition-soustraction) |
| 10 | Multiplication par 4 |
| 11 | Division par 4 |
| 12 | Multiplication par 5 |
| 13 | Division par 5 |
| 14 | Regroupement astucieux (multiplication) |
| 15 | Regroupement astucieux (addition) |
| 16 | Distributivité |
| 17 | Pourcentages |

#### Comment interpréter la "Consigne libre" et les questions imposées

Reste **toujours dans le périmètre ci-dessus**. Selon ce qui est écrit :
- **Accent sur certaines notions** (ex. "surtout les pourcentages et la distributivité") : mets davantage de questions sur ces notions, le reste librement réparti.
- **Répartition forcée** (ex. "8 questions sur les pourcentages, 1 distributivité, 1 priorités") : produis exactement ces quantités. **Avant de générer, vérifie que le total correspond au nombre de questions demandé. Si ce n'est pas le cas, ne génère rien : signale l'écart et demande une correction.**
- **Consigne vide** : propose une révision équilibrée sur l'ensemble des notions, en donnant la priorité aux plus exigeantes et les plus récentes (priorités de calcul, regroupements astucieux, distributivité, pourcentages).
- **Question(s) à inclure obligatoirement** : si le champ est rempli, reprends ces calculs **exactement tels quels**, sans les modifier, et complète le reste jusqu'au nombre demandé.

#### Règles de difficulté

- Difficulté **progressive** : commence facile, termine plus difficile.
- **Les 2 premières questions doivent être faciles** : l'élève doit toujours avoir un démarrage abordable.
- Répartition indicative : environ **un tiers de questions faciles, un tiers de moyennes, un tiers de difficiles** (par exemple, pour 10 questions : 3 faciles, 4 moyennes, 3 difficiles). Adapte ces proportions au nombre demandé.

#### Règles par notion (à respecter scrupuleusement)

**Priorités de calcul (notion 9)**
- Au moins 4 nombres dans le calcul.
- Insiste sur les calculs **sans parenthèses**, où il faut bien repérer les multiplications. Exemples : `5 × 4 − 3 × 6 + 2 =` ; `77 − 2 × 6 + 5 =` ; `18 + 4 − 3 × 3 =`.
- Inclus des enchaînements **soustraction puis addition**, pour entraîner le calcul de **gauche à droite**. Piège classique : pour `18 − 3 × 4 + 2`, on calcule d'abord `18 − 12 + 2`, puis on continue de gauche à droite : `6 + 2 = 8`. Il ne faut **pas** regrouper `12 + 2` (ce qui donnerait `18 − 14 = 4`, une erreur fréquente).

**Regroupement astucieux — multiplication (notion 14)**
- Au minimum **4 facteurs**.
- **Ne place pas côte à côte** les facteurs qui doivent se regrouper astucieusement. Exemple correct : `0,5 × 8,4 × 4 × 5` (on regroupe mentalement `0,5 × 4 × 5`). À éviter : `0,5 × 4 × 8,4 × 5` (regroupement trop évident).

**Regroupement astucieux — addition (notion 15)**
- Au minimum **4 termes**.
- Compléments à l'unité ou à la dizaine. Exemple : `4,7 + 12 + 5,3 + 8 =` (mentalement `(4,7 + 5,3) + (12 + 8) = 10 + 20 = 30`). Ne mets pas côte à côte les termes à regrouper.

**Distributivité (notion 16)**
- Uniquement des multiplications par une **puissance de 10 ± 1** : ×9, ×11, ×99, ×101, ×999, ×1001…
- Le facteur multiplié ne doit pas être trop compliqué à ajouter/soustraire (ex. `43 × 11` est bon car `430 + 43 = 473` est faisable de tête ; `987 × 11` est trop dur).
- Tout calcul du type `×9`, `×99`, `×999`… relève de **cette** notion (même s'il ressemble à une multiplication par 4 ou 5). Exemple : `4 × 999` est une question de distributivité, et la correction doit présenter la méthode de distributivité.

**Pourcentages (notion 17)**
- Forme des questions : **"X % de N"** (ex. `25 % de 200`), **sans aucune unité**.
- Pourcentages de base autorisés : 1 %, 2 %, 3 %, 5 %, 10 %, 20 %, 25 %, 40 %, 50 %, 60 %, 75 %, 80 %, 100 %.
- Pourcentages composés autorisés, par décomposition : par addition (`52 % = 50 % + 2 %` ; `15 % = 10 % + 5 %`) ou par complément à 100 % (`99 % = 100 % − 1 %` ; `98 % = 100 % − 2 %`).
- Les **résultats doivent être des nombres entiers** (tolérance : un décimal simple avec 1 %, 5 % ou 10 %).
- Varie la taille des nombres ; pour 50 %, ils peuvent être grands (jusqu'à l'ordre de 10 000).

#### Écriture des nombres (à la française)

- Virgule pour les décimales : `2,5` (et non `2.5`).
- Espace pour les milliers : `47 047` (et non `47047`).
- Symboles `×` pour multiplier et `÷` pour diviser. N'utilise aucun code LaTeX (pas de `\times`, etc.).

#### Méthodes de calcul mental à donner dans la correction

Pour chaque question, donne la réponse **et** une explication de la méthode mentale. Sois **explicite et pédagogique** : rappelle la règle utilisée (pas seulement le résultat), pour que l'élève comprenne *pourquoi* la méthode marche.

**Réflexe à encourager systématiquement — l'ordre de grandeur (garde-fou).** Avant ou après le calcul, on arrondit les nombres pour estimer rapidement le résultat attendu, et on se dit "je dois tomber sur un résultat proche de telle valeur". Cela permet de détecter une grosse erreur (virgule mal placée, zéro oublié…). Quand c'est pertinent, **ajoute cette estimation dans la correction**. Exemples : `52 % de 200` → "c'est un peu plus que la moitié de 200, donc un peu plus de 100 ; on attend ~104" ; `43 × 11` → "c'est environ `43 × 10 = 430`, donc le résultat doit être un peu au-dessus de 430" ; `12 ÷ 1000` → "on divise par 1000, le résultat doit être tout petit, autour de 0,01".

Points clés à mobiliser :

- **Priorités de calcul** : rappelle que **la multiplication et la division sont prioritaires sur l'addition et la soustraction** : on les effectue donc en premier. **Une fois les multiplications/divisions faites, on enchaîne l'addition et la soustraction de gauche à droite** (sans regrouper artificiellement). Détaille le calcul étape par étape. Exemple : `18 − 3 × 4 + 2` → on calcule d'abord `3 × 4 = 12`, donc `18 − 12 + 2` ; puis de gauche à droite : `18 − 12 = 6`, puis `6 + 2 = 8`. (Erreur à éviter : faire `12 + 2 = 14` puis `18 − 14 = 4`.)
- **±99, ±101…** : on ajoute (ou retire) la centaine/le millier le plus proche, **puis on ajuste de 1**, car `99 = 100 − 1` et `101 = 100 + 1`. Exemple : `340 + 99 = 340 + 100 − 1 = 440 − 1 = 439`.
- **× / ÷ par 10, 100, 1000** : on **décale la virgule** d'autant de rangs qu'il y a de zéros — vers la droite si on multiplie, vers la gauche si on divise. Exemple : `4,063 × 100 = 406,3` ; `12 ÷ 1000 = 0,012`.
- **× 4** : `× 4 = × 2 × 2`, donc on double deux fois. **÷ 4** : `÷ 4 = ÷ 2 ÷ 2`, on prend deux fois la moitié. Exemple : `117 × 4 = 234 × 2 = 468`.
- **× 5** : `× 5 = × 10 ÷ 2` (multiplier par 10 puis prendre la moitié). **÷ 5** : `÷ 5 = × 2 ÷ 10` (doubler puis diviser par 10). Exemple : `64 × 5 = 640 ÷ 2 = 320`.
- **Distributivité** : rappelle la règle **`k × (a + b) = k × a + k × b`** (et `k × (a − b) = k × a − k × b`). On écrit le facteur "presque rond" comme une puissance de 10 ± 1, puis on distribue. Exemples :
  - `43 × 11 = 43 × (10 + 1) = 43 × 10 + 43 × 1 = 430 + 43 = 473`.
  - `63 × 9 = 63 × (10 − 1) = 630 − 63 = 567`.
  - `4 × 999 = 4 × (1000 − 1) = 4000 − 4 = 3996`.
- **Pourcentages** : rappelle que **« X % de N » veut dire `X/100 × N`**, et qu'on simplifie la fraction `X/100` pour calculer de tête. Détaille la simplification :
  - **50 %** : `50/100 = 1/2`, donc 50 % = la moitié → diviser par 2.
  - **25 %** : `25/100 = 1/4`, donc 25 % = le quart → diviser par 4 (ou prendre deux fois la moitié).
  - **75 %** : `75/100 = 3/4`, donc 75 % = trois quarts → calculer 25 % puis multiplier par 3.
  - **20 %** : `20/100 = 1/5`, donc 20 % → diviser par 5 (ou diviser par 10 puis multiplier par 2).
  - **10 %** : `10/100 = 1/10` → diviser par 10. **1 %** : `1/100` → diviser par 100.
  - **5 %** : moitié de 10 %. **2 %** : `1 %` puis × 2. **3 %** : `1 %` puis × 3.
  - **40 % et 60 %** : à partir de 20 % (× 2, × 3) ou de 10 %. **80 %** : 10 % puis × 8.
  - **Pourcentages composés** : on décompose en parts simples puis on additionne/soustrait. Exemples : `52 % de N = 50 % de N + 2 % de N` ; `99 % de N = 100 % de N − 1 % de N` (soit `N` moins 1 % de N).

#### Historique des interrogations déjà données (référence de calibrage)

Voici toutes les interrogations déjà passées en classe (de la plus récente à la plus ancienne). **Inspire-t'en** pour : le **niveau** attendu, l'**esprit** des exercices et le **style** des énoncés. Ne fais ni monter ni baisser la difficulté par rapport à ces exemples. Produis des questions **du même esprit mais nouvelles** (varie les nombres ; ne recopie pas une interrogation entière à l'identique). Cet historique confirme aussi quelles notions ont réellement été testées — reste dans ce périmètre.

```
Interrogation N°17

10 % de 918 273 =
50 % de 360 =
7 × 101 =
25 % de 120 =
20 % de 450 =

24 × 11 =
75 % de 80 =
52 % de 200 =
98 % de 150 =
45 × 9 =

Interrogation N°16

10 % de 230 =
50 % de 480 =
5 % de 60 =
20 % de 150 =
15 % de 80 =

25 % de 160 =
2 % de 400 =
11 % de 300 =
99 % de 200 =
60 % de 200 =

Interrogation N°15

25 % de 80 =
10 % de 542 =
50 % de 7 400 =
60 % de 15 =
25 % de 240 =

20 % de 350 =
23 - 4 × 5 + 8 =
75 % de 160 =
80 % de 250 =
35 × 99 =

Interrogation N°15 - Archived

24 × 5 =
21 + 3 × 10 - 6 =
32 × 99 =
46 × 5 =
25 × 11 =

54 - 4 × 8 + 5 =
0,5 × 7 × 4 × 6 =
128 × 5 =
5 × 9 - 3 × 4 + 6 =
18 × 101 =

Interrogation N°14

36 - 5 × 4 + 7 =
7 × 3 - 4 × 5 + 6 =
12 ÷ 1 000 =
53 - 6 × (8 - 3) =
43 × 11 =

63 × 9 =
1 001 × 47 =
0,5 × 8,4 × 4 × 5 =
4,7 + 12 + 5,3 + 8 =
96 ÷ 4 =

Interrogation N°13

8 × 6 − 3 × 5 + 4 =
45 − 2 × 7 + 6 =
24 − 12 − 4 × 3 =
(19 − 6) × 2 + 3 × 2 =
5 × (9 − (3 + 3)) × 2 =

48 × 9 =
35 × 101 =
23 × 11 =
14 − 3 × 3 + 1 =
3 × (6 × 2 - 11) =

Interrogation N°12

17 × 9 =
3 508 + 199 =
4,063 × 100 =
(18 − 6) × 2 + 3 × 2 =
3 × 999 =

24 × 4 =
125 ÷ 5 =
2,5 × 6 × 4 × 2 =
27 × 11 =
5 × 4 – 3 × 6 + 2 =

Interrogation N°11

17 × 9 =
77 - 2 × 6 + 5 =
18 + 4 - 3 × 3 =
2 × (3 + 8 × 6) =
22 × 11 =

3 × ((4 + 7) - 4 × 2) =
14 × 101 =
4 × 999 =
5 × 4 – 3 × 6 + 2 =
17 × 11 =

Interrogation N°10

79 × 9 =
813 × 11 =
16 + 4 × 2 + 5 =
5 × 4 – 3 × 6 + 2 =
3 406 + 199 =

1 504 − 399 =
2,5 × 5,1254 × 4 =
92,2 + 100 + 6,8 =
92 ÷ 4 =
74 ÷ 5 =

Interrogation N°9

145 ÷ 5 =
428 ÷ 4 =
7,2 × 5 =
0,084 × 1000 =
2,5 × 6 × 4 + 18 =

0,3 + 26 + 4,7 =
3 406 + 199 =
127 + 399 =
23 × 4 =
(17 − 6) × 2 + 3 × 2 =

Interrogation N°8

12 004 ÷ 4 =
65 × 5 =
4,2 + 4 + 13,8 =
(14 + 7) × 4 =
3 208 − 201 =

620 ÷ 5 =
2,5 × 6,89 × 4 =
127 + 399 =
4,72 × 1000 =
(18 − 6) × 2 + 3 × 2 =

Interrogation N°7

35 + 4,6 + 10 + 0,4 =
90 ÷ 5 =
(15 − 7) × 3 + 5 =
64 × 5 =
7,2 × 1000 =

0,6 × 5 + 27 =
865 ÷ 100 =
2,5 × 6,68 × 4 =
34,18 × 1000 =
105 ÷ 5 =

Interrogation N°6

40 + 5,8 + 0,2 + 9 =
76 ÷ 4 =
(12 − 3) × 2 + 4 =
84 162 ÷ 100 =
117 × 4 =

88,6 × 1000 =
12 ÷ 1000 =
4 + 2 × (5 − 1) =
34,18 × 1000 =
0,5 × 44 × 4 =

Interrogation N°4 et N°5

41 × 4 =
2,5 × 6,68 × 4 =
284 ÷ 4 =
21 + 3,1 + 79 + 0,9 =
2,58 × 1 000 =

4,06 × 100 =
96 ÷ 4 =
25 + (7 − (3 + 2)) =
897 ÷ 1000 =
3 × (10 − 2) + (7 − 4) =

Interrogation N°3

7 452 ÷ 1 000 =
3 504 − 201 =
4 673 − 2 001 =
8 127 + 799 =
2,5 × 1 000 =

46 × 100 =
0,37 ÷ 100 =
2,58 × 1 000 =
897 ÷ 1000 =
276 + 101 =

Interrogation N°2

234 + 99 =
1 289 − 101 =
2 789 − 1 001 =
1 828 − 399 =
9 368 + 599 =

4,32 × 100 =
9 861 ÷ 1 000 =
34 × 100 =
89 ÷ 100 =
1,7 × 1000 =

Interrogation N°1

19 + 6 =
278 − 5 =
234 + 99 =
1 263 + 101 =
3 974 − 1 001 =

858 − 99 =
13 891 + 8 =
967 + 21 =
7 + 6 =
2 658 + 299 =
```

### Ce que tu dois produire

Une **seule** interrogation (pas plusieurs versions), en deux parties bien séparées.

**1. L'énoncé** (les questions pour l'élève)
- Un titre, puis les questions **numérotées de 1 à N**, une par ligne, **sans les réponses**.
- Respecte la difficulté progressive et les 2 premières questions faciles.

**2. La correction** (pour le parent)
- Une section nettement séparée de l'énoncé.
- Pour chaque question : le calcul, la **réponse**, et une **courte méthode** mentale (utile pour aider l'élève).

Respecte le **format de sortie** demandé :

- **Markdown** : affiche directement l'énoncé puis la correction dans la conversation.
- **PDF** : essaie d'abord de produire un **vrai fichier PDF téléchargeable** en **utilisant ton outil d'exécution de code (Python)** : génère le PDF avec une bibliothèque (`reportlab`, `fpdf2` ou `matplotlib`), enregistre-le, et **fournis le lien de téléchargement**. Mets l'énoncé sur une page et la correction sur la page suivante.
  - Si tu n'as **pas** d'outil pour créer un fichier (ex. version gratuite), **ne prétends pas avoir fait un PDF**. Dis simplement en une phrase que tu ne peux pas générer de fichier, puis affiche une version **propre et prête à imprimer** (titre clair, énoncé numéroté, puis la correction nettement séparée) et indique à l'utilisatrice qu'elle peut obtenir un PDF en faisant **Imprimer → Enregistrer au format PDF** (`Ctrl + P` / `Cmd + P`) dans son navigateur.

### Exemple de rendu attendu (mini-interrogation de 3 questions)

**Énoncé**

1. 340 + 99 =
2. 50 % de 80 =
3. 43 × 11 =

**Correction**

1. `340 + 99 = 439` — Méthode : comme `99 = 100 − 1`, on ajoute 100 puis on enlève 1 → `340 + 100 = 440`, puis `440 − 1 = 439`.
2. `50 % de 80 = 40` — Méthode : « 50 % de 80 » signifie `50/100 × 80`, et `50/100 = 1/2`. Donc 50 %, c'est la moitié → `80 ÷ 2 = 40`.
3. `43 × 11 = 473` — Méthode (distributivité) : on utilise `k × (a + b) = k × a + k × b`. Ici `43 × 11 = 43 × (10 + 1) = 43 × 10 + 43 × 1 = 430 + 43 = 473`.
