---
name: fiche_exercice_googledoc
description: Transcrit un exercice depuis un screenshot et l'ajoute a un Google Doc (texte + tableau ou image inline). Utiliser quand l'utilisateur fournit un URL Google Doc + screenshot d'exercice.
---

## Quand activer ce skill

Activer des que l'utilisateur :
- fournit un **URL de Google Doc** + un **screenshot** d'exercice a ajouter
- demande d'ajouter / transcrire / incorporer un exercice dans une fiche Google Docs
- mentionne `/fiche_exercice_googledoc`

## Inputs attendus

1. **URL du Google Doc** : URL complete ou ID du document
2. **Screenshot** : chemin vers le fichier image (PNG, JPG, etc.) ou image collee dans la conversation
3. **Titre de section** (optionnel) : le theme de l'exercice (ex: "Passage a l'unite", "Surface au sol - Montant des charges"). Si non fourni, demander a l'utilisateur.

## Script utilitaire

Toutes les operations Google Docs passent par le script :
```
~/.claude/scripts/gdoc_exercise.py
```

Commandes disponibles :
- `get-styles <doc>` — affiche les styles du document (font, taille)
- `get-end-index <doc>` — affiche l'index de fin du document
- `append-heading <doc> <text> [--level N]` — ajoute un heading (defaut H3)
- `append-text <doc> <text> [--bold-prefix N]` — ajoute un paragraphe, N premiers chars en gras
- `append-table <doc> <json>` — ajoute un tableau (JSON inline ou fichier)
- `append-image <doc> <image_path> [--width N]` — upload image sur Drive + insert inline

Le venv est dans `~/.claude/scripts/.venv/`. Executer avec :
```bash
cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py <commande> <args>
```

## Workflow

### Etape 1 — Lire le screenshot

1. Utiliser le tool `Read` pour voir le screenshot (multimodal).
2. Analyser le contenu de l'exercice :
   - Y a-t-il du texte lisible ?
   - Y a-t-il un tableau ?
   - Y a-t-il des elements graphiques (figures geometriques, schemas) impossibles a transcrire en texte ?

### Etape 2 — Decider : transcription ou image

**Cas A — Transcription possible** (texte + tableau optionnel) :
- L'exercice contient du texte et eventuellement un tableau de donnees
- Pas de figure/schema complexe
- -> Passer a l'etape 3A

**Cas B — Transcription impossible** (figure geometrique, schema, graphique complexe) :
- -> Passer a l'etape 3B

### Etape 3A — Transcrire et inserer en texte

1. **Ajouter le heading** (Titre 3) avec le theme de l'exercice :
   ```bash
   cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-heading "<doc_url>" "Theme de l'exercice"
   ```

2. **Ajouter le texte de l'exercice** :
   Le prefixe "Exercice n°X :" doit etre en **gras**. Compter le nombre de caracteres du prefixe (incluant les espaces et les deux-points) et le passer en `--bold-prefix`.
   ```bash
   cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-text "<doc_url>" "Exercice n°1 : Un transporteur propose les tarifs suivants :" --bold-prefix 16
   ```

3. **Ajouter le tableau** (si present) :
   Construire le JSON avec `headers` (premiere ligne du tableau) et `rows` (lignes de donnees).
   Le fond de l'en-tete est vert clair par defaut (comme dans les screenshots de reference).
   ```bash
   cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-table "<doc_url>" '{"headers": ["Distance (km)", "100", "150", "200", "250"], "rows": [["Couts (EUR)", "83,60", "125,40", "159,20", "191"]]}'
   ```

4. **Ajouter le texte apres le tableau** (si applicable, ex: question) :
   ```bash
   cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-text "<doc_url>" "Le prix paye est-il proportionnel a la distance parcourue ? Justifier votre reponse."
   ```

### Etape 3B — Inserer le screenshot comme image

1. **Ajouter le heading** (Titre 3) avec le theme :
   ```bash
   cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-heading "<doc_url>" "Theme de l'exercice"
   ```

2. **Inserer l'image** inline dans le document :
   ```bash
   cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-image "<doc_url>" "/chemin/vers/screenshot.png" --width 400
   ```
   La largeur par defaut est 300pt (~10.6cm). Ajuster selon la taille du screenshot.

### Etape 4 — Confirmer

Afficher a l'utilisateur :
- Ce qui a ete ajoute (heading + texte/tableau ou heading + image)
- Le lien vers le Google Doc pour verification

## Regles de transcription

- **"Exercice n°X :"** : toujours en gras (utiliser `--bold-prefix`)
- **Tableaux** : respecter exactement les valeurs du screenshot, y compris les virgules decimales
- **Symboles** : `€` pour les euros, pas `EUR` dans le texte visible (mais `EUR` dans le JSON si necessaire pour echapper)
- **Accents** : respecter l'orthographe exacte du screenshot
- Les questions posees apres un tableau sont un paragraphe separe

## Exemples

### Exemple 1 : Exercice avec tableau (transcription)

Input : screenshot montrant un exercice sur la proportionnalite avec un tableau Distance/Couts

```bash
# 1. Heading
cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-heading "https://docs.google.com/document/d/xxx/edit" "Passage a l'unite"

# 2. Texte de l'exercice (prefix en gras)
cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-text "https://docs.google.com/document/d/xxx/edit" "Exercice n°11 : 4 metres de tissu ont coute 67,5 EUR. Combien coutent 7 metres du meme tissu ?" --bold-prefix 17
```

### Exemple 2 : Exercice avec schema (image)

Input : screenshot d'un exercice de geometrie avec une figure

```bash
# 1. Heading
cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-heading "https://docs.google.com/document/d/xxx/edit" "Triangles et angles"

# 2. Image
cd ~/.claude/scripts && .venv/bin/python gdoc_exercise.py append-image "https://docs.google.com/document/d/xxx/edit" "/tmp/exercice_geo.png" --width 400
```
