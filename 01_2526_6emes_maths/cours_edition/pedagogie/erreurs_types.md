# Pédagogie — erreurs types de Claude

Historique des erreurs ou maladresses commises par Claude lors de la rédaction de cours, avec la règle généralisée à appliquer ensuite.

## Mode d'emploi

À chaque fois que l'utilisateur corrige Claude sur un point qui pourrait se reproduire (formulation, structure, exemple inadapté, niveau de langue), Claude propose : "J'ajoute à `erreurs_types.md` ?". Si oui, créer une entrée selon le template ci-dessous.

## Template d'une entrée

```
### YYYY-MM-DD — Titre court de l'erreur

**Contexte** : où Claude a fait l'erreur (chapitre, section, type de contenu).

**Ce que Claude a écrit** : citation ou résumé.

**Correction de l'utilisateur** : citation ou résumé.

**Règle généralisée** : la règle à appliquer dans les sessions futures.

**Cas d'application** : quand cette règle entre en jeu (toutes les sections ? un chapitre ? un type de bloc ?).
```

## Entrées

### 2026-05-18 — write-section casse la numérotation auto des H2 voisins

**Contexte** : push de la section "Graphique linéaire" du chap 6 (Gestion de données) via `gdoc.py write-section`. Le Doc avait initialement une numérotation auto UPPER_ROMAN sur les 4 H2 (Introduction / Tableau / Représentations / Probabilités) affichant "I. / II. / III. / IV.".

**Ce qui s'est passé** : après le `write-section` sur "Graphique linéaire" (qui est un H3 enfant de "Représentations graphiques"), les H2 "Représentations graphiques" et "Probabilités" se sont retrouvés dans une nouvelle liste auto distincte de celle d'"Introduction", démarrant à `startNumber=1`. Résultat affiché dans Docs :
- "I. Introduction"
- "II. Tableau à double entrée" (manuel, intact)
- "I. Représentations graphiques" ← cassé (devrait être III)
- "II. Probabilités" ← cassé (devrait être IV)

**Cause probable** : le `deleteContentRange` exécuté par `write-section` pour vider la section ciblée englobe le saut de ligne final, ce qui semble dissocier les paragraphes suivants de leur liste auto. À confirmer par une investigation plus poussée.

**Limite API découverte au passage** : `createParagraphBullets` ne permet **pas** de rattacher un paragraphe à une liste existante (chaque appel crée une nouvelle liste). `startNumber` est immuable post-création et non spécifiable à la création. Donc on **ne peut pas** réparer "tout-en-auto" via API.

**Règle généralisée** :
1. Avant tout `write-section` qui modifie une section enfant d'un H2 numéroté en auto, **lire les H2 voisins** et noter leurs `listId` + `startNumber` effectifs.
2. Après le push, **re-vérifier** que les H2 voisins sont toujours dans leur liste d'origine. Si non : signaler le breaking à l'utilisateur immédiatement (avant de continuer).
3. Pour les chapitres où la numérotation H2 doit rester stable malgré des éditions de sections enfants : **préférer une numérotation manuelle** ("I. Introduction" écrit en dur dans le texte) plutôt qu'une liste auto. La numérotation manuelle survit aux `write-section`.

**Fix appliqué** (chap 6) : passage des 3 H2 affectés en numérotation manuelle ("I. ", "III. ", "IV. " écrits en dur dans le texte, avec `deleteParagraphBullets` pour retirer la liste auto résiduelle).

**Cas d'application** : tous les chapitres qui utilisent une liste auto numérotée pour les H2. À vérifier sur l'index des chapitres si d'autres docs sont concernés.

---

### 2026-05-18 — Tableau poussé en format "pipe `|`" au lieu de table native

**Contexte** : 1er push de la section "Graphique linéaire", chap 6. Le tableau a été rédigé en format texte avec séparateurs `|` au lieu d'un vrai tableau Google Docs natif.

**Règle généralisée** : pour tout tableau dans un cours, **toujours utiliser `gdoc_insert_table.py`** (qui produit un tableau natif Docs stylé selon les conventions de `formatting_guide.md`). **Jamais** rédiger un tableau en pipes texte dans le contenu passé à `gdoc.py write-section` — c'est inesthétique et nécessite une conversion manuelle.

**Cas d'application** : toute insertion de données tabulaires (tableau de valeurs, comparaisons, tableau de proportionnalité, etc.).

---

### 2026-05-18 — Consignes d'exercice rédigées à l'impératif au lieu de l'infinitif

Voir aussi `pedagogie/langage.md` (section "Consignes d'exercice : verbes à l'infinitif"), qui détaille la règle. Documenté ici aussi pour rappel : **toujours infinitif** dans les listes d'instructions de type "À toi de jouer. ...".

---

### 2026-05-19 — Le skill edition_cours ne couvrait pas la création initialement

**Contexte** : demande de "créer un Google Doc Chapitre 12 sur Périmètres et aires dans tel dossier Drive". Le skill v1 (créé le 2026-05-18) ne couvrait que l'édition de Docs existants — aucune commande pour créer un nouveau Doc.

**Ce qui a été fait** : création à la volée d'un nouveau script `gdoc_create.py` (Drive API `files().create()` + Docs API `batchUpdate` pour pousser un squelette markdown-like avec styles Montserrat 12/14/16/18 pt). Puis enrichissement du SKILL.md avec une "Étape 2a — Créer un nouveau Doc" et élargissement du trigger d'activation.

**Règle généralisée** : quand un cas non couvert par le skill se présente, deux choses sont nécessaires en parallèle :
1. Faire le travail (créer le script / la commande manquante).
2. **Étendre le skill** pour que ce cas soit couvert la prochaine fois — sinon on refera le diagnostic à chaque session future.

**Cas d'application** : tout cas où le skill `edition_cours` est invoqué pour une action qu'il ne décrit pas explicitement. Faire systématiquement les 2 étapes ci-dessus, ne pas se contenter de "ça marche pour cette fois".

**Anti-pattern à éviter** : faire l'action sans documenter, en se disant "on retrouvera le code". Le skill EST la documentation discoverable — un script orphelin ne l'est pas.

---

### 2026-05-19 — Conventions visuelles (gras, couleur, numérotation) non extraites des Docs existants

**Contexte** : création du squelette Chapitre 12. Claude a appliqué Montserrat aux niveaux de heading mais a oublié 3 dimensions visuelles importantes :
- **Gras** sur H1, H2, H3
- **Couleurs** : H1 noir, H2 bleu `#0000ff`, H3 magenta `#ff00ff`
- **Alignement** : H1 centré
- **Numérotation H3** : "1. ", "2. ", … en chiffres arabes simples, réinitialisée à chaque H2 (pas "I.1", "I.2")

L'utilisateur a dû les énoncer après-coup.

**Cause racine** : `gdoc.py read` retourne uniquement le texte. La V1 du `formatting_guide.md` a été construite à partir de cette lecture surfacique et avait des TODOs "à confirmer" qui n'ont jamais été comblés. Claude s'est contenté de l'incomplet.

**Règle généralisée — extraction des conventions visuelles** :
1. À la première session sur un projet de cours (et après chaque ajout d'un nouveau type de bloc), **inspecter le JSON brut** d'au moins un Doc existant pour extraire : couleurs (`textStyle.foregroundColor`), gras (`textStyle.bold`), alignements (`paragraphStyle.alignment`), tailles (`textStyle.fontSize`).
2. **Ne pas se contenter** du texte retourné par `gdoc.py read`. Pour le styling, descendre dans le JSON via `docs.documents().get(documentId=X)` et parcourir `body.content[].paragraph.elements[].textRun.textStyle`.
3. **Demander à l'utilisateur** quand un doute persiste (la lecture API ne dit pas tout : nuances de couleur perçues, conventions implicites comme "le titre est toujours centré").

**Sous-erreur connexe — interprétation des options AskUserQuestion** : quand l'utilisateur choisit une option du type *"Réinitialisée à chaque H2 (I.1, I.2, I.3, I.4 / II.1, II.2, II.3)"*, le contenu entre parenthèses est un **exemple illustratif de la logique**, pas la convention typographique exacte. Confirmer le rendu exact (formatage du préfixe) avant d'implémenter, surtout pour les éléments qui apparaîtront dans le rendu final.

**Cas d'application** :
- Toute nouvelle session de création de Doc → vérifier que `formatting_guide.md` est exhaustif (pas de "à confirmer" résiduel).
- Toute lecture de Doc existant → si on doit reproduire le style, faire une inspection JSON, pas une lecture texte.

---

### 2026-05-19 — Bug "saut de ligne résiduel" avant chaque insertTable

**Contexte** : insertions séquentielles de tableaux et encadrés (qui utilisent aussi `insertTable` sous le capot) dans la section I.1 du chap 12. Entre chaque "phrase d'amorce" (ancre) et le tableau/encadré inséré juste après, un saut de ligne **vide visible** apparaît dans le rendu Docs.

**Cause technique** : l'API Google Docs `insertTable` insère **systématiquement un caractère `\n` implicite** avant le tableau créé. Documentation Google : *"Inserts a new table at the specified location. A newline character is inserted before the table."* Ce `\n` génère un paragraphe vide entre l'ancre et le tableau.

**Règle généralisée** : après chaque `insertTable` (que ce soit pour une vraie table, ou pour un encadré via `gdoc_insert_box.py`), **toujours nettoyer** le paragraphe vide intercalaire :
1. Re-lire le doc post-`insertTable`.
2. Identifier la position du tableau créé.
3. Vérifier si le paragraphe juste avant est vide (texte = "" ou "\n").
4. Si oui : `deleteContentRange` sur ce paragraphe vide.

Implémenté dans `gdoc_insert_table.py` et `gdoc_insert_box.py` à compter du 2026-05-19.

**Cas d'application** : toute insertion de tableau ou d'encadré dans un Doc. Les scripts modifiés gèrent ça automatiquement, mais à garder en tête si on écrit un nouveau script qui appelle `insertTable` directement.

---

### 2026-05-19 — Bug "insertText texte vide" rejeté par l'API

**Contexte** : tentative de pousser un tableau de conversion avec lignes vides (les élèves doivent remplir). Le CSV avait des cellules vides. `gdoc_insert_table.py` envoyait des `insertText {text: ""}` qui faisaient échouer le batch entier (`HTTP 400 — Insert text requests must specify text to insert`).

**Règle généralisée** : avant tout `insertText`, **filtrer les chaînes vides**. Les laisser tomber silencieusement (la cellule reste vide nativement, ce qui est l'effet voulu).

Implémenté dans `gdoc_insert_table.py` à compter du 2026-05-19 (liste `requests` construite avec une condition `if text`).

**Cas d'application** : tout script qui génère des `insertText` à partir de données potentiellement partielles (CSV, JSON, etc.). Toujours filtrer avant d'envoyer le batch.

---

### 2026-05-19 — Interligne 1,5 mal adapté aux lignes à trous

**Contexte** : push de I.1 avec `--line-spacing 150` pour donner de la place aux élèves d'écrire dans les trous. Retour utilisateur : l'interligne 1,5 sur un paragraphe de 1 seule ligne ne crée aucune place utilisable. Inefficient et gaspille de la verticalité.

**Règle généralisée** : pour donner de la place à écrire au-dessus d'une ligne à trous, utiliser `paragraphStyle.spaceAbove` (par exemple 12 pt) plutôt que `lineSpacing: 150`. L'espace est créé entre le paragraphe précédent et le paragraphe à trous — vraie zone d'écriture.

`lineSpacing` reste pertinent pour des paragraphes **multi-lignes** où on veut aérer entre les lignes (rare en cours à trous).

`gdoc.py write-section` détecte désormais automatiquement les paragraphes contenant `…………` et leur applique `spaceAbove: 12pt`. Voir `formatting_guide.md` section "Interligne et espacement".

**Cas d'application** : tout push qui contient des lignes à trous → on n'a plus besoin de spécifier `--line-spacing 150` manuellement (la détection est automatique).

---

### 2026-05-19 — Indentation hiérarchique manquante (Headings et sous-éléments)

**Contexte** : retour utilisateur sur le rendu de I.1 — les Headings et les sous-éléments numérotés (`1. ` `2. ` dans Méthode, `a. ` `b. ` dans Exercice) sont tous alignés à gauche, pas de vraie hiérarchie visuelle.

**Cause** : Google Docs n'applique pas d'indentation par défaut aux Headings. Et les paragraphes commençant par `N. ` ou `lettre. ` ne sont pas reconnus comme sous-éléments — Docs les voit comme du texte normal.

**Règle généralisée** : appliquer `paragraphStyle.indentStart` explicite selon le niveau hiérarchique. Voir `formatting_guide.md` section "Indentation hiérarchique" pour les valeurs exactes (H3 = 18, texte = 36, sous-éléments = 54 pt).

`gdoc.py write-section` et `gdoc_insert_box.py` détectent désormais automatiquement les paragraphes commençant par `N. ` ou `lettre. ` et leur appliquent `indentStart: 54pt`.

**Cas d'application** : tout push de contenu structuré (méthodes pas-à-pas, énoncés multi-questions, listes alphabétiques).

---

### 2026-05-19 — Sur-utilisation des encadrés colorés (fatigue visuelle)

**Contexte** : proposition initiale de design avec 7 types d'encadrés colorés (À retenir, Définition, Méthode, Rappel, Attention, Exemple, Exercice). Retour utilisateur : trop de couleurs, saturation.

**Règle généralisée** :
1. **5 encadrés "à fond coloré"** suffisent (À retenir / Définition / Méthode / Rappel / Attention).
2. Pour les **Exemples** et **Exercices** : pas d'encadré complet. Juste **label gras + couleur + barre verticale colorée à gauche** (`paragraphStyle.borderLeft`). Convention dite "Option B" — voir `formatting_guide.md`.

**Principe** : pour éviter la fatigue visuelle, n'utiliser un encadré complet **que quand le contenu est de nature différente du texte courant** (à retenir, méthode, attention, etc.). Pour les exemples et exercices, qui sont une **continuation du texte courant** avec une nature différente (à comprendre, à faire), un repère visuel léger suffit.

**Cas d'application** : tout choix de design d'une nouvelle convention visuelle — préférer le moins lourd qui distingue suffisamment.

---

### 2026-05-19 — `write-section` écrase les modifications manuelles de l'utilisateur

**Contexte** : itération sur la section I.1 du chap 12. À chaque retour utilisateur, Claude re-pousse via `write-section` qui efface tout le contenu existant et le remplace. Si l'utilisateur a modifié manuellement quelque chose dans le Doc entre 2 pushs (correction d'une formulation, ajout d'un exemple personnel, etc.), ces modifications sont **détruites silencieusement**.

**Cause technique** : `gdoc.py write-section` exécute `deleteContentRange` sur toute la plage entre le heading et le suivant, puis insère le nouveau texte. Pas de merge, pas de diff.

**Règle généralisée** : par défaut, ne **jamais** utiliser `write-section` sur une section déjà rédigée. Utiliser à la place :
- `replaceAllText` (via script ad-hoc) pour modifier une phrase précise
- `insertText` à un index ancré pour ajouter un paragraphe
- `gdoc_insert_box.py` / `gdoc_insert_table.py` pour ajouter un encadré ou un tableau
- `gdoc_apply_styles.py` pour ré-appliquer les conventions visuelles sans toucher au texte
- `updateTextStyle` / `updateParagraphStyle` ciblé pour modifier un style sur un range précis

`write-section` est réservé à la **1ère rédaction** d'une section vide ou à l'instruction explicite *"réécris toute cette section"*. Voir `.claude/skills/edition_cours/SKILL.md` Étape 4 — Push pour la règle d'or et le tableau de décision.

**Avant tout `write-section` itératif** : demander à l'utilisateur s'il a modifié manuellement le Doc depuis le dernier push. Si oui, basculer obligatoirement sur des opérations chirurgicales.

**Cas d'application** : toute session d'itération sur une section existante. Particulièrement critique en fin de chapitre quand l'utilisateur ajuste et personnalise au fur et à mesure.
