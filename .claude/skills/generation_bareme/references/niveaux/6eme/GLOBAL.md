# Mémoire barème — 6ème (règles transverses + index des chapitres)

Règles de notation valables sur **toute** interro/DS de 6ème, indépendamment du chapitre.
Enrichi à chaque passage du skill (capitalisation). Ne consigner ici que ce qui est
**réutilisable** (généralisable), jamais une pénalité liée à une valeur numérique d'un sujet.

## Logique de notation (rappel)

- Barème majoritairement **soustractif** ; crédits partiels notés `x/y` ; plancher 0 par question.
- Points max **tirés de l'énoncé** (`\question[..]`, `\part[..]`).
- Toute démarche / explication de "comment j'aurais résolu si j'avais eu telle information" est
  **valorisée** quand l'énoncé l'indique (boîtes `Indication` du sujet).

## Règles transverses (tous chapitres)

### Questions de cours / définitions
- Oubli d'un **élément clé** de la définition : pénalité lourde (≈ −1,5 sur 2, à l'échelle).
- Phrase **syntaxiquement incorrecte** ou notion clairement non intégrée : −0,5 (jusqu'à −1,5 si très confus).
- Toute réponse approximative sur une question de cours marquée "vocabulaire mathématique attendu" peut valoir 0.

### Questions de raisonnement marquées `[Justifier]` (`\just`)
- **Valeur correcte donnée sans aucune justification** : crédit partiel ≈ `0,25/1` (à l'échelle des points de la question).
- **Justification incomplète** (propriété du cours mobilisée mais non citée explicitement) : ≈ `0,5/1`.
- **Propriété du cours non citée** alors qu'elle est le cœur du raisonnement : −0,5 (à l'échelle).
- **Erreur de calcul** avec démarche correcte : pénalité légère (−0,5 ou moins), la démarche reste valorisée.
- Ne **pas cumuler** les pénalités jusqu'à l'absurde si la réponse finale est correcte.

### Figures / tracés
- Légende ou codage manquant : −0,5 par élément, **plafonné** (≈ −2) si récurrent ; pénaliser en priorité les codages qui servent à construire/justifier.
- Construction faite à la règle là où le **compas** est attendu : pénalité globale (≈ −1).
- Figure sale / traits pas droits : −0,25 à −1,5 selon gravité.
- Oubli d'**unité** (cm, °) dans un résultat chiffré : −0,5.

## Index des chapitres

Lire le `.md` du chapitre dès qu'un titre d'exercice (`\section*{Exercice N - <thème> ...}`)
matche un déclencheur ci-dessous.

| Fichier chapitre | Déclencheurs (mots-clés des titres / énoncés) |
|---|---|
| `chapitres/mediatrice_bissectrice_cercle.md` | médiatrice, bissectrice, cercle circonscrit, définition de cours géométrique |
| `chapitres/symetrie_axiale.md` | symétrie axiale, symétrique, axe de symétrie, tracé par rapport à une droite |
| `chapitres/angles_triangle.md` | angles du triangle, somme des angles, isocèle, équilatéral, calculer un angle |
| `chapitres/longueurs_perimetre.md` | longueurs, périmètre, côtés égaux |

Pour ajouter un chapitre : créer `chapitres/<nom>.md`, puis ajouter sa ligne ci-dessus avec
ses déclencheurs.
