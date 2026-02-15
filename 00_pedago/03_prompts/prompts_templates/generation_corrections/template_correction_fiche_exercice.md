TEMPLATE DE PROMPT – GENERATION DE CORRIGE LaTeX (Mathématiques 6ème)

# CONTEXTE GENERAL

Je suis professeur de mathématiques en classe de 6ème.
Je souhaite que tu génères un corrigé détaillé et pédagogique d’exercices à partir de captures d’écran, sous la forme d’un unique fichier LaTeX compilable, conforme à un squelette précis.


# TACHE

Générer un unique fichier LaTeX compilable contenant le corrigé des exercices fournis.
Tu dois respecter strictement :
- le template de document LaTeX imposé
- les conventions d’écriture LaTeX
- les règles de rédaction mathématique adaptées à des élèves de 6ème

# RESULTAT ATTENDU (OBLIGATOIRE)

- Un unique fichier LaTeX compilable
- Chaque section correspond exactement à un exercice
- Le document respecte strictement le squelette fourni
- Le corrigé est écrit pour des élèves de 6ème avec un raisonnement détaillé

# Classe LaTeX exam

- Version énoncé uniquement : \documentclass{exam}
- Version avec corrigé : \documentclass[answers]{exam}
- Tu ne dois rien inventer en dehors du squelette fourni.

# DONNEES FOURNIES

- Matière : Mathématiques
- Classe : 6ème
- Titre : [TEMPLATE]
- Path Exercice 1 (respecter exactement ce path) : [#INSERER]
- Path Exercice 2 (respecter exactement ce path) : [#INSERER]

# CONTRAINTES TEMPLATE LaTeX (STRUCTURE DU DOCUMENT)

- Tu dois impérativement utiliser le template LaTeX fourni
- Tu dois remplacer toutes les variables (ex : [TITRE], [DATE], [CLASSE])
- Tu ne dois ni supprimer ni ajouter de commandes structurelles

Template obligatoire : [INSERER TEMPLATE LATEX 03_prompts/contraintes/contraintes_template_latex.tex]

# GESTION DES IMAGES (OBLIGATOIRE)

- Chaque exercice doit contenir obligatoirement sa figure
- La figure est placée juste après le titre de la section
- Utiliser systématiquement la commande suivante :
\fig{0.6}{path}{Titre de la figure}
- Le path correspond exactement au chemin fourni
- Cette convention ne doit jamais être modifiée

# CONTRAINTES DE REDACTION MATHEMATIQUE

- Structure obligatoire du raisonnement
- Dès qu’une justification est nécessaire, le raisonnement doit suivre strictement la structure suivante :
  - On sait que (Hypothèses utiles issues de l’énoncé ou des questions précédentes)
  - Or (Propriété mathématique utilisée // Préciser dans quelle figure ou dans quel triangle on se place)
  - Donc (Conclusion logique)


- Tu dois respecter strictement les consignes de rédactions définies dans le fichier suivant :

[INSERER CONTRAINTES LATEX
03_prompts/contraintes/contraintes_redaction_maths.md]

# Justifications attendues

- Toute utilisation d’une propriété mathématique doit être explicitement justifiée
- Il faut toujours préciser le contexte géométrique exact
- Les résultats démontrés dans les questions précédentes peuvent être réutilisés, mais doivent être explicitement cités


# CONTRAINTES ECRITURE / LIBRAIRIES LaTeX

- Tu dois respecter strictement les conventions définies dans le fichier suivant :

[INSERER CONTRAINTES LATEX
03_prompts/contraintes/contraintes_format_latex.md]


# NIVEAU PEDAGOGIQUE ATTENDU

- Niveau fourni dans les données
- Aucune étape implicite
- Calculs très détaillés
- Vocabulaire simple et précis
- Raisonnement progressif et explicite

# EXEMPLE DE MODE DE REDACTION

- Le style de rédaction doit être cohérent avec le fichier exemple fourni
- En cas de doute, expliquer davantage plutôt que moins

Fichier exemple :
[FICHIER DE CORRECTION FOURNI]
