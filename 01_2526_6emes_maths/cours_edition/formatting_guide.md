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

## Polices, tailles, couleurs et alignement

Convention typo **complète** des Google Docs de cours (à appliquer à tout contenu poussé via API). Mise à jour 2026-05-19.

| Élément | Police | Gras | Taille | Couleur | Alignement | Numérotation |
|---|---|---|---|---|---|---|
| **Heading 1** (titre du chapitre) | Montserrat | ✓ | 20 pt | `#000000` noir | **Centré** | — |
| **Heading 2** (grandes parties) | Montserrat | ✓ | 16 pt | `#0000ff` bleu pur | (défaut, gauche) | **Romaine manuelle** : "I. ", "II. ", "III. " écrits en dur dans le texte |
| **Heading 3** (sous-sections) | Montserrat | ✓ | 14 pt | `#ff00ff` magenta | (défaut, gauche) | **Arabe manuelle** : "1. ", "2. ", … écrits dans le texte. Compteur **réinitialisé à chaque H2** (donc il peut y avoir plusieurs "1." dans le doc, séparés par leurs sections). Pas de préfixe romain ("I.1") — juste le chiffre. |
| Texte normal (paragraphes) | Montserrat | (non) | 12 pt | (défaut, noir) | (défaut, gauche) | — |

**Pourquoi numérotation manuelle** : la numérotation auto Docs (`createParagraphBullets` avec preset UPPER_ROMAN) se casse facilement quand on modifie une section enfant via `write-section`. Voir `pedagogie/erreurs_types.md` (entrée 2026-05-18). La numérotation manuelle survit aux éditions.

**Implémentation API** : pour chaque heading, appliquer dans un `updateTextStyle` les 4 propriétés :
```json
{
  "bold": true,
  "weightedFontFamily": {"fontFamily": "Montserrat"},
  "fontSize": {"magnitude": <size>, "unit": "PT"},
  "foregroundColor": {"color": {"rgbColor": {"red": R, "green": G, "blue": B}}}
}
```
avec `fields: "bold,weightedFontFamily,fontSize,foregroundColor"`.

Pour H1 : également un `updateParagraphStyle` avec `alignment: "CENTER"`.

Le simple `insertText` n'applique aucun style — toujours faire suivre par les `updateTextStyle` et `updateParagraphStyle` adaptés sur le range inséré.

## Tableaux

Convention pour les tableaux Google Docs natifs :

| Élément | Valeur |
|---|---|
| Police | Montserrat |
| Taille | 10 pt (plus petit que le texte courant) |
| Alignement horizontal (toutes cellules) | Centré |
| Alignement vertical (toutes cellules) | Centré (`contentAlignment: MIDDLE`) |
| Marge intérieure (padding) | 0,1 cm sur les 4 côtés (≈ 2,83 pt) |
| **Header (1ère ligne)** | Gras |
| **Header (1ère ligne)** | Couleur de remplissage `#c9daf8` (bleu clair pastel) |

**Implémentation API** : appliquer dans cet ordre après `insertTable` + remplissage des cellules :
1. `updateTextStyle` Montserrat 10pt sur la plage du tableau
2. `updateParagraphStyle alignment: CENTER` sur la plage du tableau
3. `updateTableCellStyle contentAlignment: MIDDLE` + padding 2,83 pt sur toutes les cellules (`tableRange` couvrant n_rows × n_cols)
4. `updateTableCellStyle backgroundColor: #c9daf8` sur la 1ère ligne (`rowSpan: 1`)
5. `updateTextStyle bold: true` sur les cellules de la 1ère ligne

### Règle : tableau présent dans une image source → reconstruire en natif

Quand on s'inspire d'une ressource pédagogique (PDF, photo de page de cours, screenshot) qui contient un **tableau** que l'on souhaite intégrer dans le Doc :

**Ne PAS** insérer l'image du tableau via `gdoc_insert_image.py`.

**À FAIRE** : lire visuellement le contenu du tableau dans la source, recomposer un CSV à partir des données extraites, et l'insérer en **tableau Docs natif** via `gdoc_insert_table.py`. Le tableau aura ainsi la convention typo standard (header bleu, données centrées, Montserrat 10pt) — cohérent avec le reste du cours, modifiable par l'utilisateur, et plus net visuellement qu'une capture d'écran.

S'applique aussi aux **tableaux de conversion**, **tableaux de formules**, **tableaux de valeurs** rencontrés dans Yvan Monka, manuels scolaires, photos de cours existants. La règle ne s'applique PAS aux schémas géométriques, figures, dessins — ceux-ci doivent rester en images via `gdoc_insert_image.py`.

## Exercices dans le cours

Convention de présentation des exercices (et de leurs corrections) dans le Doc du cours.

**Règle 1 — Texte par défaut.** Quand un exercice peut être restitué sous forme de texte (énoncé seul + données numériques + question), **toujours le rédiger en texte** dans le Doc plutôt qu'en image. Plus modifiable, plus lisible, cohérent avec le reste du cours.

**Règle 2 — Screenshot quand image indispensable.** Si l'exercice contient une **figure géométrique**, un **schéma annoté**, ou un **tableau de valeurs riche** qu'il serait fastidieux de retranscrire fidèlement en texte, alors **screenshoter** depuis la source (PDF, photo de manuel) via le workflow `_crops/` (voir section "Workflow screenshots"). Insérer ensuite l'image via `gdoc_insert_image.py`.

**Règle 3 — Espace blanc en dessous (obligatoire).** Pour permettre à l'élève de **faire l'exercice ou écrire la correction directement dans le Doc imprimé**, laisser **un espace blanc de quelques lignes** sous chaque énoncé. En pratique : insérer 3 à 6 paragraphes vides après l'énoncé (ajustable selon la nature de l'exercice : 3 lignes pour un calcul simple, 6+ pour une rédaction).

**Cas particulier — tableau à compléter** : si l'exercice est un tableau à remplir (ex : tableau de conversion vide), utiliser `gdoc_insert_table.py` avec des cellules vides plutôt qu'un screenshot. Cela garde la convention typo et permet à l'élève de remplir directement s'il édite en ligne.

## Encadrés

Convention transverse à tous les cours. 5 types d'encadrés, tous implémentés via une **table Google Docs 1×1** avec fond, bordure et padding `0,15 cm`. Le label (titre de l'encadré) est inséré dans la cellule en gras, suivi du contenu en texte normal.

| Type | Fond | Bordure | Label | Usage |
|---|---|---|---|---|
| **A. À retenir** | `#fff2cc` (jaune pâle) | `#ffa500` orange, épaisse | "À RETENIR" gras orange centré | Fin de chaque grande section — synthèse formules / règles clés à mémoriser |
| **B. Définition** | `#e8f4f8` (bleu très pâle) | `#0000ff` bleu (assorti H2) | "Définition" gras bleu | Notion clé à mémoriser (périmètre, aire, π, formules nommées) |
| **C. Méthode** | `#d9ead3` (vert pâle) | `#38761d` vert moyen | "Méthode" gras vert | Procédure pas-à-pas, en général numérotée |
| **D. Rappel** | `#f0f0f0` (gris pâle) | `#999999` gris | "Rappel" italique gris | Lien explicite avec un chapitre précédent (ex : "rappel du chap 4 sur les fractions") |
| **E. Attention** | `#ffe5e5` (rouge pâle) | `#cc0000` rouge | "⚠ Attention" gras rouge | Piège fréquent / erreur classique (ex : conversions d'aires à 2 rangs vs 1) |

**Justification du code couleur** : aligné sur la palette existante des headings (H2 bleu → encadré Définition bleu, H3 magenta → C en vert pour distinguer méthode de sous-section). Jaune/gris/rouge sont les codes universels (highlight / aside / warning).

**Implémentation API** : utiliser `~/.claude/scripts/gdoc_insert_box.py` qui crée la table 1×1 et applique le styling complet en une commande :
```
gdoc_insert_box.py <URL> \
    --section "<section>" \
    --after-text "<phrase d'ancrage>" \
    --type {a-retenir,definition,methode,rappel,attention} \
    --content "<texte du corps>" \
    --account perso
```

Le label ("À RETENIR", "Définition", etc.) est ajouté automatiquement — ne pas l'écrire dans `--content`.

## Interligne et espacement (révisé 2026-05-19)

### Espace avant les paragraphes à trous (privilégier sur l'interligne 1,5)

L'**interligne** uniforme 1,5 ne sert à rien sur un paragraphe d'une seule ligne (cas typique des trous). Préférer un **espace avant** le paragraphe (`paragraphStyle.spaceAbove`), qui crée une vraie zone d'écriture libre au-dessus.

| Contenu | Méthode | Valeur API |
|---|---|---|
| **Paragraphes contenant `…………` (trous à remplir)** | Interligne simple (100) + `spaceAbove: 12pt` | `lineSpacing: 100` + `spaceAbove: {magnitude: 12, unit: "PT"}` |
| **Paragraphes texte continu (sans trous)** | Interligne simple (100), pas d'espace supplémentaire | `lineSpacing: 100` |

**Détection automatique** : `gdoc.py write-section` détecte les paragraphes contenant `…………` (séquence d'ellipses) et leur applique `spaceAbove: 12pt` automatiquement. Pas besoin de flag manuel.

L'ancienne convention "interligne 1,5 sur tout le texte à trous" est **dépréciée** : ça gaspille de la place verticale sur les paragraphes longs sans aider à l'écriture.

## Indentation hiérarchique (ajoutée 2026-05-19)

Les Headings Google Docs n'ont pas d'indentation native. Pour créer une vraie hiérarchie visuelle, appliquer `paragraphStyle.indentStart` selon le niveau :

| Niveau | Indentation gauche | Cas concret |
|---|---|---|
| H1 (titre chapitre) | 0 pt (centré) | "Chapitre 12 - …" |
| H2 (grande section) | 0 pt | "I. Périmètres" |
| H3 (sous-section) | 18 pt | "1. Unités de longueur" |
| Paragraphes texte sous H3 | 36 pt | Définitions, méthodes, énoncés |
| **Sous-éléments numérotés** (`1. `, `2. `, `a. `, `b. `) | 54 pt | Étapes de méthode, sous-questions d'exercice |

**Détection automatique** : `gdoc.py write-section` détecte les paragraphes commençant par `[a-z]\. ` ou `[0-9]+\. ` et leur applique `indentStart: 54pt`. Idem dans `gdoc_insert_box.py` (contenu des encadrés).

## Design des Exemples et Exercices (ajouté 2026-05-19)

Pour distinguer visuellement Exemples résolus et Exercices d'application **sans saturer le doc en couleur**, convention "Option B" : label gras + barre verticale colorée à gauche, **pas d'encadré complet**.

| Type | Label | Couleur (label + barre) | Largeur barre |
|---|---|---|---|
| **Exemple N (descripteur)** | "Exemple N (...)" en gras | `#1c4587` (bleu marine) | 3 pt |
| **Exercice ...** | "Exercice ..." en gras | `#b45f06` (orange foncé) | 3 pt |

**Implémentation API** :
- `updateTextStyle` sur le préfixe (jusqu'au `:` ou jusqu'à la fin du label) avec `bold: true` + `foregroundColor`
- `updateParagraphStyle.borderLeft` sur le paragraphe entier avec `color` + `width: 3pt` + `dashStyle: SOLID` + `padding: 6pt`

**Détection automatique** dans `gdoc.py write-section` :
- Paragraphes commençant par `Exemple ` (avec espace) → style Exemple
- Paragraphes commençant par `Exercice ` (avec espace) → style Exercice

## Tableaux multi-questions (révisé 2026-05-19)

Quand un même tableau de résolution sert pour plusieurs sous-questions (a, b, c…) ou exemples consécutifs, **mettre une seule table avec N lignes vides** au lieu de N tables séparées. C'est plus économe visuellement, plus rapide à parcourir, et plus simple côté API.

Exemple : exercice "Compléter a. 5,6 m = … cm  /  b. 28 dm = … dam" → **1 tableau de 2 lignes vides** (1 ligne pour a, 1 ligne pour b), pas 2 tables séparées.

## Interligne (ancienne section, dépréciée)

Voir "Interligne et espacement" ci-dessus. Le flag `--line-spacing 150` reste disponible dans `gdoc.py write-section` pour cas particuliers, mais la valeur par défaut (100) + détection automatique du `spaceAbove` sur lignes à trous est désormais la convention.

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
