---
name: generation_calcul_mental
description: Génère une interrogation de calcul mental de 6ème (10 questions, 4 versions shufflées) et écrit le fichier LaTeX compilable. Produit énoncé + correction.
---

## Modes d'utilisation

### Mode 1 — Générer une nouvelle interrogation

```
/generation_calcul_mental <numéro_interro> <date> "<consigne>"
```

La `<consigne>` est un texte libre qui pilote le contenu de l'interro — voir la
section « La consigne (3ᵉ argument) » ci-dessous.

Exemples :
- `/generation_calcul_mental 14 "16 Avril 2026" "9, 16"`
- `/generation_calcul_mental 15 "13 Mai 2026" "8 questions sur les pourcentages, 1 distributivité, 1 priorités de calcul"`

### Mode 2 — Recompiler un devoir existant (énoncé + correction)

```
/generation_calcul_mental <chemin_vers_fichier.tex>
```

Exemple : `/generation_calcul_mental 01_2526_6emes_maths/00_calcul_mental/interro_calcul_mental_14.tex`

Dans ce mode, sauter directement à l'**Étape 3** (compilation).

---

## La consigne (3ᵉ argument)

Le 3ᵉ argument du Mode 1 est un **texte libre**. L'IA l'interprète et le classe dans
l'un des régimes suivants (les combinaisons sont autorisées) :

- **Notions prioritaires (accent)** — une liste de notions, par numéro ou par nom
  (ex : `"9, 16"` ou `"priorités et distributivité"`). L'IA répartit librement les
  10 questions en mettant l'accent sur ces notions.

- **Répartition forcée (exacte)** — des comptes précis par notion
  (ex : `"8 questions sur les pourcentages, 1 distributivité, 1 priorités de calcul"`).
  L'IA génère **exactement** ces quantités. Le total **doit valoir 10** ; si ce n'est
  pas le cas, **STOP** et demander une correction à l'utilisateur.

- **Questions imposées** — des énoncés exacts à inclure tels quels
  (ex : `"impose 32 × 99 et 1001 × 47"`). Ces énoncés apparaissent sans modification ;
  les questions restantes complètent jusqu'à 10.

- **Consigne vide** — accent par défaut sur les notions 9 à 16.

Voir `references/pedagogie.md` pour la liste numérotée des notions et leurs contraintes.

---

## Workflow — Mode 1 (nouvelle interrogation)

### Étape 1 — Générer et MONTRER les questions (STOP après cette étape)

1. **Lire** le fichier de référence pédagogique : `references/pedagogie.md` (relatif à ce skill)
2. **Interpréter la consigne** (3ᵉ argument — voir la section dédiée) : déterminer le
   régime (notions prioritaires, répartition forcée, questions imposées, ou combinaison).
   - Si la consigne est une **répartition forcée**, vérifier que le total vaut **exactement 10**.
     Sinon : **STOP**, signaler le total obtenu et demander une correction à l'utilisateur.
   - **Reformuler l'interprétation** à l'utilisateur avant de générer les questions.
3. **Générer 10 questions** en respectant toutes les contraintes de `references/pedagogie.md`
   - Niveau 6ème, réalisable mentalement en < 30 secondes (< 50 s pour les pourcentages)
   - Difficulté progressive : 3 faciles, 4 moyennes, 3 difficiles
   - Respecter la consigne passée en argument
   - Aucune question déjà présente dans l'historique des interros
4. **Calculer les réponses** pour chaque question
5. **Afficher les 10 questions** et **ATTENDRE la validation** :

```
Questions proposées pour l'Interrogation #<N> :

 1. 8 × 6 − 3 × 5 + 4 =        → 37  (Priorités de calcul)
 2. ...
10. ...

Valides-tu ces questions ?
```

**NE PAS passer à l'étape 2 tant que l'utilisateur n'a pas validé.**

### Étape 2 — Écrire le fichier LaTeX

Une fois les questions validées :

1. **Lire le template** : `references/template.tex` (relatif à ce skill)
2. **Créer 4 permutations** (shuffles) différentes des 10 questions
3. **Pour chaque permutation** : questions 1–5 dans `\qcol` gauche, 6–10 dans `\qcol` droite
4. **Écrire le fichier .tex** dans `01_2526_6emes_maths/00_calcul_mental/`
   - Nom : `interro_calcul_mental_<N>.tex`
   - Remplacer `\interronum` et `\interrodate` par les valeurs
   - Remplacer les `\emptystudentblock` par les 4 `\studentblock` remplis
   - **Utiliser la macro `\q{expression}{réponse}`** pour chaque question (pas d'expression nue)

### Étape 3 — Compiler et produire les 2 PDFs

**Toujours produire 2 PDFs** (que ce soit mode 1 ou mode 2) :

```bash
DIR="01_2526_6emes_maths/00_calcul_mental"
FILE="interro_calcul_mental_<N>"

# 1. Énoncé (sans réponses)
cd "$DIR" && pdflatex -interaction=nonstopmode -halt-on-error "$FILE.tex"
mv "$FILE.pdf" "[6eme] Interrogation <N> - Enonce.pdf"

# 2. Correction (avec réponses en rouge gras)
pdflatex -interaction=nonstopmode -halt-on-error "\def\showanswers{}\input{$FILE.tex}"
mv "$FILE.pdf" "[6eme] Interrogation <N> - Correction.pdf"
```

Ouvrir les 2 PDFs avec `open`.

Afficher le corrigé texte :
```
Corrigé — Interrogation #<N> :
 1. 8 × 6 − 3 × 5 + 4 = 37          (Priorités de calcul)
 ...
```

---

## Format LaTeX des questions — macro `\q`

Chaque question utilise la macro `\q{expression}{réponse}` :
- En mode énoncé : seule l'expression s'affiche
- En mode correction : l'expression suivie de la réponse en **rouge gras**

```latex
\q{$36 - 5 \times 4 + 7 =$}{23}
```

Conventions pour l'expression :
- Mode math : `$...$`
- Multiplication : `\times`
- Division : `\div`
- Virgule décimale : `{,}` (ex: `$2{,}5 \times 4 =$`)
- Séparateur de milliers : `\,` (ex: `$3\,508 + 199 =$`)
- Chaque expression se termine par ` =$`

La réponse est en texte brut (pas en mode math) : `23`, `0,012`, `47 047`

## Exemple de sortie .tex (partie document)

```latex
\renewcommand{\interronum}{14}
\renewcommand{\interrodate}{16 Avril 2026}

\noindent
\begin{tabular}{@{}c@{}c@{}}
  \studentblock
    {\qcol{\q{$36 - 5 \times 4 + 7 =$}{23}}
          {\q{$7 \times 3 - 4 \times 5 + 6 =$}{7}}
          {\q{$12 \div 1\,000 =$}{0,012}}
          {\q{$53 - 6 \times (8 - 3) =$}{23}}
          {\q{$43 \times 11 =$}{473}}}
    {\qcol{\q{$63 \times 9 =$}{567}}
          {\q{$1\,001 \times 47 =$}{47 047}}
          {\q{$0{,}5 \times 8{,}4 \times 4 \times 5 =$}{84}}
          {\q{$4{,}7 + 12 + 5{,}3 + 8 =$}{30}}
          {\q{$96 \div 4 =$}{24}}}
  & \studentblock{...version 2 shufflée...}{...}
  \\[-\arrayrulewidth]
  \studentblock{...version 3...}{...}
  & \studentblock{...version 4...}{...}
\end{tabular}
```

## Robustesse

- Toutes les contraintes de `references/pedagogie.md` sont respectées
- La difficulté est homogène avec les interros précédentes
- Aucune question de l'historique n'est réutilisée
- Les calculs sont faisables mentalement en < 30 secondes
- Les réponses calculées sont exactes
- Le nombre de questions est exactement 10
