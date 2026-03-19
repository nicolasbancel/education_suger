# Génération d'interrogations de calcul mental – Mathématiques 6e

Ce prompt génère des interrogations de calcul mental adaptées au niveau 6e. Remplissez uniquement la section ci-dessous, puis envoyez le prompt tel quel à l'IA (Claude, ChatGPT, etc.).

## A remplir par le parent ou l'élève

### Nombre de questions

> 15

### Notions prioritaires

Indiquez les numéros des notions sur lesquelles vous souhaitez insister (ex : `9, 14, 16`).
Si vous laissez vide, l'IA répartira automatiquement les questions avec un accent sur les notions 9 à 16.

| # | Notion |
|---|--------|
| 1 | Addition simple |
| 2 | Soustraction simple |
| 3 | Addition (+99, +199, +299...) |
| 4 | Addition (+101, +1001...) |
| 5 | Soustraction (-99, -199, -299...) |
| 6 | Soustraction (-101, -201, -1001...) |
| 7 | Multiplication par 10, 100, 1000 |
| 8 | Division par 10, 100, 1000 |
| 9 | Priorités de calcul |
| 10 | Multiplication par 4 |
| 11 | Division par 4 |
| 12 | Multiplication par 5 |
| 13 | Division par 5 |
| 14 | Regroupement astucieux (multiplication) |
| 15 | Regroupement astucieux (addition) |
| 16 | Distributivité |

> *(remplacez cette ligne par vos numéros, ou laissez vide)*

### Questions obligatoires à inclure

Si vous souhaitez imposer certaines questions exactes dans l'interrogation, écrivez-les ci-dessous (une par ligne). Sinon, laissez vide.

> *(remplacez cette ligne par vos questions, ou laissez vide)*

**Ne modifiez rien en dessous de cette ligne — les instructions ci-dessous sont destinées à l'IA.**

## Role

Tu es un **enseignant de Mathématiques en classe de 6e (collège)**.
Tu aides à la **génération d'interrogations hebdomadaires de calcul mental**, adaptées au niveau des élèves.

Les calculs doivent pouvoir être réalisés mentalement en moins de 30 secondes par un élève moyen de 6e (je leur donne une interrogation toutes les semaines : 10 questions, à faire en 5 minutes). Aucun calcul ne doit nécessiter de technique écrite (division posée, multiplication posée complexe…). Ils n'ont évidemment pas le droit à la calculette.

Si le parent utilise la même fenêtre et le même contexte pour générer de nouvelles questions, aucun calcul déjà présent dans l'historique ne doit être réutilisé.

## Contexte pédagogique et contraintes

Les notions déjà travaillées en classe sont les suivantes :

1. Addition simple
2. Soustraction simple
3. Addition avec un terme du type 99, 199, 299, 399, etc.
4. Addition avec un terme du type 101, 1001, etc.
5. Soustraction avec un terme du type 99, 199, 299, etc.
6. Soustraction avec un terme du type 101, 201, 1001, etc.
7. Multiplication par 10, 100, 1000
8. Division par 10, 100, 1000
9. Priorités de calcul (parenthèses / multiplication / soustraction).
    - Sur les calculs de priorités, je veux voir au moins 4 chiffres, voire plus
    - Insiste un peu plus sur des calculs où il n'y a pas de parenthèse du tout, et où il faut bien distinguer où sont les multiplications. Exemples :
        - 5 × 4 – 3 × 6 + 2 =
        - 77 - 2 × 6 + 5 =
        - 18 + 4 - 3 × 3 =
    - Inclus aussi des calculs où la priorisation implique aussi un enchaînement de soustraction et d'addition. Les élèves ont tendance à d'abord effectuer les additions (parce que c'est plus simple) plutôt que de traiter le calcul de gauche à droite. Par exemple, pour : 18 - 3 x 4 + 2, il font 18 - 12 + 2 (priorité à la multiplication), mais font ensuite 18 - 14 (en effectuant l'opération 12 + 2 d'abord, et mettant artificiellement des parenthèses : 18 - (12 + 2)), alors qu'il faut effectuer simplement le calcul de gauche à droite : 18 - 12 + 2 = 6 + 2 = 8.
10. Multiplication par 4
11. Division par 4
12. Multiplication par 5
13. Division par 5
14. Regroupement astucieux (multiplication)
    - Exemples : 2,5 × 4 ; 0,2 × 5 ; 0,5 × 4 ; 0,125 × 8 ; 0,1 × 10
    - Au minimum 4 facteurs
    - Ne mets pas côte à côte les facteurs qui doivent être regroupés astucieusement
15. Regroupement astucieux (addition)
    - Compléments à l'unité ou à la dizaine (ex : 0,2 + 3,8)
    - Au minimum 4 termes
    - Ne mets pas côte à côte les termes qui doivent être regroupés astucieusement
16. Distributivité
    - Uniquement des multiplications par une puissance de 10 + 1 ou -1 (Exemples : × 9, × 11, × 101, × 99, × 1001, × 999...)
    - Dans le cas d'un Y × 11 ou Y × 9 (et n'importe quel autre scénario de ce type), le facteur Y ne doit pas être trop complexe à ajouter ou à soustraire à 10 × Y

## Objectif

Génère **une nouvelle interrogation de calcul mental** respectant strictement les contraintes suivantes :

- Le nombre de questions est celui indiqué dans la section "A remplir" en haut du document
- **Le niveau de difficulté doit être équivalent à celui des interrogations précédentes, sans augmentation nette ni simplification excessive.**
- Mettre un accent particulier sur les notions prioritaires indiquées dans la section "A remplir" en haut du document
- Si aucune notion prioritaire n'est fournie, répartis les questions selon l'importance pédagogique générale, avec un accent sur les notions 9 à 16.
- Les questions obligatoires indiquées dans la section "A remplir" doivent apparaître **exactement telles quelles**, sans modification.

## Référence de niveau

Tu trouveras ci-dessous l'historique complet des interrogations précédentes. Il sert uniquement à :
- comprendre le niveau attendu
- respecter l'esprit des exercices
- éviter toute montée ou baisse de difficulté

```
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

79  9 =
813 x 11 =
16 + 4 × 2 + 5 =
5 × 4 – 3 × 6 + 2 =
3 406 + 199 =

1 504 − 399 =
2,5 × 5,1254 × 4  =
92,2 + 100 + 6,8 =
92 ÷ 4 =
74 ÷ 5 =

Interrogation N°9

145 ÷ 5 =
428 ÷ 4 =
7,2 × 5 =
0,084 x 1000 =
2,5 × 6 × 4 + 18 =

0,3 + 26 + 4,7 =
3406 + 199 =
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

19 + 6
278 − 5
234 + 99
1 263 + 101
3 974 − 1 001

858 − 99
13 891 + 8
967 + 21
7 + 6
2 658 + 299
```

## Format de sortie attendu

- Format texte sans caractères spéciaux, que je peux directement copier coller dans mon document d'interrogation, sans aucune mise en forme (type .txt)
- Tu utiliseras les signes officiels pour les additions, les soustractions, les divisions (÷ et pas /), et les multiplications (× et pas la lettre x), et les décimales sont à écrire avec une virgule, pas un point.
- Questions qui se suivent, avec numérotation (1. pour la 1ère question, 2. pour la 2ème question etc)
- A la fin, explicite ce qui est évalué par chaque question, c'est un repère pour les parents et l'élève. Par exemple 1. Distributivité. Ces notions reprennent la liste des éléments du programme énoncés dans la section "Contexte pédagogique et contraintes"
- Une multiplication par 9, 99, 199, ou par n'importe quel nombre proche d'une puisance de 10 teste nécessairement la distributivité. Si la question est 4 x 999, il est impératif de fournir la méthode associée à la distributivité, pas à la multiplication par 4.
- A la fin de chaque question, il y a un espace, un signe = et un espace. Par exemple 2,5 × 29 × 4 =
- **Aucune correction**, uniquement les énoncés

## Exemple d'output parfait

```
1. 17 × 9 =
2. 3 508 + 199 =
3. 1 204 − 399 =
4. 46 × 100 =
5. 8 400 ÷ 100 =
6. (18 − 6) × 2 + 3 × 2 =
7. 24 × 4 =
8. 125 ÷ 5 =
9. 2,5 × 6 × 4 =
10. 27 × 11 =

Notions évaluées :
1. Distributivité
2. Addition avec un terme du type 99, 199, 299, 399, etc.
3. Soustraction avec un terme du type 99, 199, 299, etc.
4. Multiplication par 10, 100, 1000
5. Division par 10, 100, 1000
6. Priorités de calcul
7. Multiplication par 4
8. Division par 5
9. Regroupement astucieux (multiplication)
10. Distributivité
```

# Robustesse

Avant de générer l'interrogation, vérifie que
- toutes les contraintes sont respectées
- la difficulté est homogène
- il n'y a pas d'erreur de notation
- le nombre de questions est correct
