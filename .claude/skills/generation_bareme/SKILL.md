---
name: generation_bareme
description: Génère le barème (CSV copiable dans Google Sheets) d'une interro / DS / DM à partir de son énoncé .tex et d'un .md d'instructions de notation, en s'appuyant sur une mémoire de barème par niveau de classe et par chapitre qu'il enrichit à chaque passage.
---

## Quand activer ce skill

Activer dès que l'utilisateur demande :
- de **générer / rédiger / produire un barème** pour un devoir (interro, DS, DM) dont l'énoncé `.tex` existe,
- de mettre à jour / régénérer un barème existant,
- de "construire la grille de notation" d'un contrôle qu'il vient de donner.

Ce skill ne corrige pas les copies (voir `correction_interro` pour la correction, `correction_dm` pour les DM numériques). Il produit **uniquement le barème**.

## Arguments

```
/generation_bareme <chemin_énoncé.tex> [<chemin_instructions.md>]
```

- **arg 1 (obligatoire)** : chemin de l'énoncé `.tex` du devoir à barémer.
- **arg 2 (optionnel mais recommandé)** : un `.md` d'**instructions de notation propres à CE contrôle** (la philosophie de barème voulue : sévérité, points sensibles, crédits partiels attendus, pièges à pénaliser). C'est lui qui aiguille la génération ET alimente la capitalisation.

Le **niveau de classe** est déduit du chemin :
- `..._6emes_...` ou `.../6eme/...` → `6eme`
- idem `5eme`, `4eme`, `3eme`.

Si le niveau ne peut pas être déduit, **demander à l'utilisateur** avant de continuer.

## Étapes obligatoires AVANT de générer (chargement du contexte)

Lire, dans cet ordre :

1. `references/format_sortie.md` — le format de sortie CSV strict (contrainte non négociable).
2. `references/baremes_modeles/6eme_interro_5.md` — barème de référence validé par l'utilisateur. Cale l'**esprit, le niveau d'exigence, la logique de notation**.
3. `references/niveaux/<niveau>/GLOBAL.md` — règles de notation transverses au niveau + **index des chapitres**.
4. **Identifier les chapitres du devoir** : lire les titres de section de l'énoncé (`\section*{Exercice N - <thème> (<points>)}`) et croiser avec les déclencheurs listés dans l'index de `GLOBAL.md`. Lire chaque `references/niveaux/<niveau>/chapitres/<chapitre>.md` correspondant.
5. Si arg 2 fourni : lire le `.md` d'instructions du contrôle.

Si `references/niveaux/<niveau>/` n'existe pas (premier barème de ce niveau) : créer le dossier, partir d'un `GLOBAL.md` minimal calqué sur celui de 6ème, et le signaler à l'utilisateur.

## Logique de notation — non négociable

- Barème **majoritairement soustractif** : pénalités `-x` pour erreurs / oublis / imprécisions.
- **Crédits partiels positifs** possibles, écrits `x/y` (ex. `0,5/1`, `1,5/3`).
- Pénalités **cumulables**, dans la limite d'un **plancher de 0** par question.
- Les **points maximaux viennent de l'énoncé** : valeur entre crochets de chaque `\question[..]` / `\part[..]`. Ne jamais inventer un total ; la somme des points max doit égaler le total annoncé dans les titres d'exercices.
- **Référencement** systématique et complet : `Exercice 1`, `Question 2`, sous-question `a`, `b`… (`ExNQM` = Exercice N, Question M ; `ExNQMa` = sous-question a).

## Workflow

1. **Charger le contexte** (section ci-dessus).
2. **Produire les lignes de barème, question par question.** Pour chaque question, croiser :
   barème modèle + `GLOBAL.md` + `chapitres/<chapitre>.md` + instructions du contrôle (arg 2).
   - **Se baser sur l'énoncé RÉEL**, pas sur les `Indication` qui peuvent contenir des reliquats copiés d'un sujet précédent (piège vu sur l'interro 6 : une `Indication` mentionnait un cercle absent du sujet).
   - Une ligne par élément de barème ; plusieurs lignes par question autorisées.
3. **Écrire le CSV** à côté de l'énoncé : `<dossier_énoncé>/<nom_énoncé>_bareme.csv` (header inclus). Sortie CSV **uniquement** — ne pas dupliquer le tableau dans le chat.
   - **Vérifier** que la somme des points max = total annoncé. Si écart : STOP, signaler, ne pas écrire un barème faux.
4. **Capitalisation (obligatoire).** Extraire de l'arg 2 (et des choix de barème faits) les règles **réutilisables** — c'est-à-dire indépendantes des valeurs numériques de CE sujet (ex. « toute valeur d'angle donnée sans citer la somme des angles = 180° → pénalité » est réutilisable ; « -0,75 si 70° donné sans justification » ne l'est pas).
   - Règle transverse au niveau → `GLOBAL.md`.
   - Règle propre à un chapitre → `chapitres/<chapitre>.md` (créer le fichier + l'entrée dans l'index de `GLOBAL.md` si le chapitre est nouveau).
   - **Montrer le diff proposé et demander validation à l'utilisateur AVANT d'écrire** dans la mémoire. Ne jamais polluer la mémoire avec du bruit non généralisable.

## Relecture finale (robustesse)

- **Virgule décimale** partout dans le barème (`-1,5`, `0,25/1`) — sinon Google Sheets n'interprète pas les nombres.
- Séparateur de colonnes : **`;`**.
- 5 colonnes exactement, dans l'ordre : `N° de l'exercice ; N° de question ; Sous-question ; Nombre de points maximal ; Barème`.
- **Nombre de points max sur la 1ère ligne de chaque question uniquement** (vide sur les lignes suivantes), pour que la somme dans Sheets reste juste.
- Aucun texte hors CSV dans le fichier.
- Apostrophes droites ASCII, guillemets droits `"..."`.
