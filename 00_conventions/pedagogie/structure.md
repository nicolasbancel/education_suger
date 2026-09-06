# Pédagogie — structure

Conventions sur la façon d'organiser une notion dans un cours de 6ème.

## Mode d'emploi

Ce fichier capture la séquence et la mise en ordre type des blocs pédagogiques. Premier amorçage à partir des chapitres 5 (Proportionnalité) et 10 (Symétrie axiale), à enrichir au fil des sessions.

## Deux styles selon le domaine

L'observation des chapitres 5 et 10 fait apparaître **deux structurations distinctes** selon la nature du contenu :

### Style inductif — pour l'arithmétique et le numérique

Observé notamment en chap 5 Proportionnalité. Séquence type :

1. **Situation concrète** ouvrant la sous-section (ex : Jade et sa taille, prix au marché)
2. **Question posée** à l'élève (proportionnel ou pas ? quelle valeur ?)
3. **Cours à trous** où l'élève est invité à formuler la conclusion lui-même
4. **Conclusion / définition** qui émerge naturellement de l'exemple
5. **Méthode** annoncée (souvent par un chiffre : "3 méthodes", suivi de la liste)
6. **Exercices d'application** intercalés ou en fin de partie

Pas de bloc "Définition" préalable séparé — la définition naît de l'exemple.

### Style déductif structuré — pour la géométrie

Observé en chap 10 Symétrie axiale. Séquence type :

1. Sous-section **`Définitions`** explicite (souvent supportée par un schéma)
2. Sous-section **`Méthode`** ou `Méthode de construction` (procédure pas-à-pas)
3. Sous-section **`Exemple et propriété`** (cas résolu débouchant sur l'énoncé d'une propriété)
4. Sous-section **`Exercice d'application`** ou `Pour vous entraîner`

Structure plus proche d'un cours de maths "classique".

## Vocabulaire des sous-sections (Heading 3)

Préférer ces formulations, déjà ancrées dans les chapitres existants :

- `Définitions` (avec un "s" final)
- `Méthode` ou `Méthode de construction`
- `Exemple et propriété`
- `Exercice d'application` ou `Exercices d'application`
- `Pour vous entraîner`
- `Introduction` (pour ouvrir une partie)

## Granularité

À documenter au fil des sessions :

- **Longueur d'un Heading 2** (grande partie) : observé entre 2 et 4 sous-sections.
- **Longueur d'un Heading 3** (sous-section) : à mesurer.
- **Cours à trous** : densité à calibrer — à enrichir.

## Annonce des méthodes multiples

Quand une notion admet plusieurs méthodes de résolution, **annoncer le nombre puis lister les noms** avant de les détailler.

Pattern type (chap 5) :
```
3 méthodes
Méthode de la multiplication ou de la division
Méthode de l'addition
Méthode du passage à l'unité
```

Puis chaque méthode est ensuite détaillée.

## Transitions entre sections

À documenter — pas encore d'observation systématique. Pour l'instant : passer d'une sous-section à l'autre via le simple Heading 3, sans phrase de transition explicite.

## Conventions structurelles d'un chapitre (ajoutées 2026-05-19)

Règles transverses à appliquer à tous les chapitres :

### 1. Intro motivante en début de chapitre

Chaque chapitre commence par un **paragraphe court** (3-6 lignes) qui répond à "à quoi ça sert ?" avec un ou deux exemples concrets du quotidien. La place : entre le H1 (titre du chapitre) et la première section H2.

But : engager l'élève dès la 1ère ligne, contextualiser la notion avant de la formaliser.

Exemple (chap 12) :
> "Pour clôturer un jardin avec du grillage, il faut mesurer le contour du terrain : on parle de **périmètre**. Pour peindre un mur, il faut mesurer la surface à couvrir : on parle d'**aire**. […]"

### 2. Exemples gradués (annoncer la difficulté)

Quand une notion admet plusieurs exemples successifs, **annoncer explicitement le niveau** : "exemple simple", "exemple plus difficile", "cas à piège". L'élève sait où il en est dans la progression.

À éviter : enchaîner 3 exemples sans marqueur, ce qui rend la perception de la difficulté implicite.

### 3. Rappels inter-chapitres (quand pertinent)

Quand une notion s'appuie sur un chapitre antérieur (ex : conversions d'aires ↔ conversions de longueurs ; calculs avec décimaux ↔ chap 1 ; pourcentages ↔ fractions chap 4), **inclure un encadré "Rappel"** explicite (gris pâle, voir `google_docs.md`).

But : sécuriser l'élève qui aurait oublié, et faire le pont mental entre chapitres.
