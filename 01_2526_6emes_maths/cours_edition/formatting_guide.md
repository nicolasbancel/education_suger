# Formatting guide — cours de 6ème (Google Docs)

Conventions de mise en forme pour les Google Docs de cours de 6ème, extraites des chapitres 4 (Fractions), 5 (Proportionnalité), 6 (Gestion de données), 9 (Triangles et quadrilatères) et 10 (Symétrie axiale) le 2026-05-18.

**Limite actuelle** : la lecture API ne récupère pas les images, les couleurs ni les styles fins (gras/italique de paragraphes intermédiaires). Ces aspects restent à documenter au fil des sessions.

## Hiérarchie de titres

Convention observée, stable d'un chapitre à l'autre :

| Niveau | Usage |
|---|---|
| **Heading 1** | Titre du chapitre, format `Chapitre N - <Titre>` (ex: `Chapitre 5 - Proportionnalité`) |
| **Heading 2** | Grandes parties thématiques (ex: `Reconnaître la proportionnalité`, `Pourcentage`, `Figures symétriques`) |
| **Heading 3** | Sous-sections (ex: `Définitions`, `Méthode de construction`, `Exercices d'application`) |
| **Heading 4** | Sous-sous-sections d'application (ex: `Application : Calculer`, `Application : Compléter`, `Exemple d'application`). Surtout utilisé en chap 4 Fractions. |

Pas de numérotation préfixée dans les titres (pas de "I.", "II.", "1.1") — la hiérarchie visuelle suffit.

**Convention de mise en exergue** : un Heading 3 ou 4 en **MAJUSCULES** signale un point d'importance forte (ex : `TRÈS IMPORTANT POUR LE CALCUL MENTAL` dans chap 4).

## Sous-sections récurrentes (Heading 3)

Vocabulaire constaté pour les Heading 3, regroupé par fonction pédagogique :

**Ouverture / contextualisation** :
- `Introduction` (chap 5, 6)
- `Familiarisation / Rappels de CM` (chap 4) — transition primaire→6ème
- `Vocabulaire` (chap 4, 9) — section dédiée au lexique

**Définition / théorie** :
- `Définitions` (avec un "s" final, chap 9, 10)
- `Théorie` (chap 4) — variante plus rare
- `Vocabulaire et propriétés` (chap 9)
- `Explication` (chap 4)

**Méthode** :
- `Méthode` ou `Méthode de construction` (chap 10)
- `Méthodes de construction` (au pluriel, chap 9)
- `Méthode - Comparaison` (chap 4)

**Exemples** :
- `Exemple` (chap 9)
- `Exemples` (chap 4)
- `Exemple et propriété` (chap 10) — exemple débouchant sur une propriété
- `Exemple et méthode` (chap 4)

**Application / entraînement** :
- `Application` ou `Applications` (chap 4, 5)
- `Exercice d'application` ou `Exercices d'application` (chap 5, 9, 10) — intercalé entre sous-sections, pas seulement en fin de partie
- `Pour vous entraîner` (chap 10)

**Heading 4 (sous-sections d'application, chap 4)** :
- `Application : Calculer`
- `Application : Compléter (sur le cahier d'exercice)`
- `Exemple d'application`

## Approches pédagogiques

Deux styles coexistent selon le domaine :

### Style inductif (arithmétique : chap 5 Proportionnalité)

- Démarre par une **situation concrète** (ex: "À 10 ans, Jade mesurait 1,20 m...")
- Pose une **question** ("Le prix est-il proportionnel à la quantité ?")
- Laisse de l'espace pour la **réflexion** (cours à trous, voir ci-dessous)
- Tire la **conclusion** : "Le tableau s'appelle un tableau de proportionnalité"
- **Pas de bloc "Définition" formel** : la définition émerge de l'exemple

### Style déductif structuré (géométrie : chap 10 Symétrie axiale)

- Sous-sections explicites : `Définitions`, `Méthode`, `Propriété`, `Exemple`
- Définitions formulées explicitement (souvent en image — schéma + texte)
- Suit la séquence : Définition → Méthode → Exemple → Exercice d'application
- Structure plus proche d'un cours de maths "classique"

**Conséquence pour la génération de contenu** : adapter au domaine. Pour proportionnalité, fractions, calcul → privilégier l'inductif. Pour géométrie → privilégier le déductif structuré.

## Cours à trous

Convention très présente : les passages destinés à être complétés par les élèves en classe sont matérialisés par des **séquences de points** (souvent avec espaces non-sécables : `………………………………………`).

Exemples relevés :
- `il a fait ……………………………………… des questions`
- `Et on note : ……………………………`
- `Quand on …..…..…..…..…..…..…..…..…..…..…..`
- `Le ……………….………. est ………….……….……….……….………. au ………..………..………..………..………..`

À respecter pour les nouvelles sections : prévoir des trous adaptés à la difficulté (un mot vs une phrase complète).

## Annonce des méthodes

Pattern observé en arithmétique : annoncer le nombre de méthodes avant de les détailler.

Exemple chap 5, section "Utiliser la proportionnalité sans tableau" :
```
3 méthodes
Méthode de la multiplication ou de la division
Méthode de l'addition
Méthode du passage à l'unité
```

Puis chaque méthode est détaillée plus bas.

## Exemples : ancrage dans le quotidien

Contextes observés (chap 5) : âge et taille, prix au marché, tours de montagne russe, course à pied, achat de stylos, longueur d'une cathédrale, examens scolaires, tablette de chocolat, anniversaires, matchs de foot, météo.

**Règle implicite** : les exemples sont **ancrés dans des situations de la vie d'un·e élève de 6ème** (sport, école, achats, animaux, monuments connus, etc.). Éviter les exemples abstraits ou décorrélés du quotidien.

## Notations typographiques

Constats :

- **Virgule décimale** : `1,20 mètres` (français standard — à respecter, ne pas écrire `1.20`)
  - ⚠️ Le chap 5 contient en réalité `1.20 mètres` (avec point) — **à vérifier avec l'auteur** si c'est volontaire ou un défaut à corriger systématiquement.
- **Apostrophe typographique** `'` (et non droite `'`) : `l'âge`, `d'application`
- **Symbole euro** : collé au nombre, `5€` (sans espace)
- **Pourcentage** : `40%`, `84%` (sans espace avant `%`)
- **Espace insécable** : présent dans les ponctuations doubles (`:`, `?`, `!`) — convention française

## Éléments non capturés par la lecture API

À ce jour, le script `gdoc.py read` ne récupère pas :
- Les **images** (schémas géométriques, illustrations, tableaux dessinés)
- Les **tables** Google Docs (les cellules sont skippées dans le parseur actuel)
- Les **couleurs**, **gras**, **italique** au sein des paragraphes
- Les **encadrés visuels** (tables 1×1 utilisées comme cadres, fond coloré, etc.)

Pour la rédaction, on procédera ainsi :
1. Texte structurel via le script Python.
2. Pour les images/schémas : les annoncer dans le texte ("Schéma à insérer : ...") et les ajouter manuellement à la finition.
3. Styles visuels : on retiendra une convention simple par type de bloc (à définir progressivement dans `pedagogie/structure.md`).
