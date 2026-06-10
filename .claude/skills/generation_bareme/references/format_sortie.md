# Format de sortie — barème CSV

Contrainte stricte. Le skill produit **un seul fichier CSV**, écrit à côté de l'énoncé
(`<dossier_énoncé>/<nom_énoncé>_bareme.csv`), directement importable dans Google Sheets.

## Les 5 colonnes (ordre imposé)

1. `N° de l'exercice`
2. `N° de question`
3. `Sous-question`
4. `Nombre de points maximal`
5. `Barème`

La **première ligne** du fichier contient le nom des 5 colonnes.

## Règles de format

- **Séparateur de colonnes** : point-virgule `;` (et pas la virgule, qui est réservée aux décimales).
- **Nombres décimaux** : écrits avec une **virgule** (`-1,5`, `0,25`, `7,2`), jamais un point — sinon Google Sheets ne les interprète pas comme des nombres.
- **Crédits partiels** : notés `x/y` (ex. `0,5/1`, `1,5/3`).
- **Une ligne par élément de barème.** Une même question peut occuper plusieurs lignes.
- **Nombre de points maximal** : renseigné uniquement sur la **1ère ligne de chaque question** (cellule vide sur les lignes suivantes de la même question), afin que la somme de la colonne reste égale au total réel du devoir.
- **Intitulés complets** : `Exercice 1`, `Question 1`, et `a`, `b`… pour les sous-questions. Pas d'abréviation dans le CSV (les abréviations `Ex1Q2`, `Ex4Q1a` servent seulement à parler du barème en langage naturel).
- **Sortie épurée** : aucun texte, commentaire ou explication hors des lignes du tableau.

## Référencement en langage naturel

Pour discuter du barème (dans le chat, dans les `.md` d'instructions ou de mémoire) :
- `Ex1Q2` = Exercice 1, Question 2
- `Ex4Q1a` = Exercice 4, Question 1, sous-question a

## Extrait d'exemple (interro 6, 6ème)

```
N° de l'exercice;N° de question;Sous-question;Nombre de points maximal;Barème
Exercice 1;Question 1;;1,5;-1,5 si oubli de la perpendicularité, du passage par le milieu, ou du fait que c'est une droite
Exercice 1;Question 1;;;-1 si "forme un angle droit" sans préciser avec quoi (terme de perpendicularité absent)
Exercice 3;Question 1;;1,5;-0,75 si la valeur (70°) est donnée sans justification
Exercice 3;Question 1;;;-0,5 si la propriété "dans un triangle, la somme des angles vaut 180°" n'est pas citée
Exercice 4;Question 3;;1;0,25/1 si la valeur (7,2 cm) est donnée sans justification
Exercice 4;Question 3;;;-0,5 si oubli de l'unité (cm)
```

Noter : les points max (`1,5`, `1`) n'apparaissent qu'une fois par question ; les lignes
suivantes laissent la colonne vide.
