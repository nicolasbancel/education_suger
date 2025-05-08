- Le texte n'est pas formatté exactement au format d'une liste de dictionnaires Python exploitable tel quel. Convertis le moi en une liste comme celle ci-dessous
- Ton output ne doit pas inclure de tique '`', ni de mention de 'python'. C'est simplement une liste de dictionnaires, avec les clés énoncées ci-dessus.


[
    {
      "numero_exercice": int,  # Numéro d’ordre de l’exercice (1 pour le 1er, 2 pour le 2e, etc.)
      "titre_exercice": str,   # Contenu brut de la balise \section{}, sans modification
      "enonce_exercice": str,  # Tout le texte situé entre \section{} et la première \question{}, sans modification
      "questions_exercice": [  # Liste contenant le contenu brut de chaque balise \question{}, dans l’ordre d’apparition
        str,  # Contenu de la première question
        str,  # Contenu de la deuxième question
        ...
      ]
    },
    ...
]
