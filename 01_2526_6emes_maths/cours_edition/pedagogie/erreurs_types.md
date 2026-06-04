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
