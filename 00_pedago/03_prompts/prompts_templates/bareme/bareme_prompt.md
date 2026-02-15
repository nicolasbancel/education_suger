Je veux que tu m’aides à rédiger un barème détaillé pour un devoir que je viens de donner à mes élèves.

# Contexte fourni

Je te fournis :

(1) Un barème d’un devoir précédent, que j’ai moi-même construit, afin que tu en respectes :
- l’esprit général,
- le niveau d’exigence,
- la logique de notation (pénalités, crédits partiels, rédaction attendue).

(2) Le sujet du devoir précédent, correspondant à ce barème.

(3) Le sujet du nouveau devoir, pour lequel tu dois produire le nouveau barème.

# Logique de notation attendue

- Le barème est majoritairement soustractif (pénalités de type -x pour erreurs, oublis, imprécisions)
- Des crédits partiels positifs sont possibles dans certains cas (sous la forme x/y (par exemple 0.5/1).)
- Les pénalités sont cumulables, dans la limite d’un score minimum de 0 pour chaque question.

# Format de sortie (contrainte stricte)

Tu dois produire exactement un seul tableau, sans aucun texte avant ou après. Le tableau doit contenir 5 colonnes, dans cet ordre :

- N° de l’exercice
- N° de la question
- Sous-question
- Nombre de points maximal
- Barème

Contraintes de format :

- La 1ère ligne doit contenir le nom des 5 colonnes
- Les nombres décimaux (dans le barème) doivent être écrits avec une virgule, et non pas un point (sinon, ils ne sont pas interprétés comme des nombres décimaux par Google Sheet)
- Le tableau doit être directement copiable dans Google Sheets. Mets un séparateur bien identifiable entre chaque colonne (point virgule, de préférence)
- Une ligne par élément de barème est attendue.
- Il peut y avoir plusieurs lignes pour une même question ou sous-question.
- Le format doit être parfaitement épuré (pas de commentaires, pas d’explications hors tableau).

# Conventions et exemple

- Utilise systématiquement les intitulés complets : Exercice 1, Question 1, a, b, etc. a, b etc font référence à des sous-questions.
- Exemple de ligne attendue

Exemples de barème soustractif

- Exercice 1
- Question 1
- b
- 2
- -0.5 si la notion de perpendicularité n'est pas mentionnée

Exemples de barème avec # total de points

- Exercice 1
- Question 1
- c
- 2
- 1/2 si la définition est faite avec les mots de l'élève mais ne respecte pas mot pour mot la définition officielle

# Données fournies
- Barème d’un devoir précédent (à prendre comme référence) : [#TEMPLATE] [6eme] Interrogation 5 - Bareme.pdf
- Sujet et correction du devoir précédent (lié au barème de référence) [#TEMPLATE] [6eme] Interrogation 5 - Correction.pdf
- Sujet du nouveau devoir (à utiliser pour produire le nouveau barème) [#TEMPLATE] [6eme] Interrogation 6 - Enonce.pdf

# Objectif final

Produire un barème cohérent avec mes pratiques, adapté au nouveau sujet, en respectant strictement le format demandé, sans ajout de texte explicatif. Il est très important d'inclure un séparateur clair pour faciliter la copie dans Google Sheets
