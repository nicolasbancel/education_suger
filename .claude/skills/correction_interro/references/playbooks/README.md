# Playbooks par type d'exercice

Chaque fichier de ce dossier décrit **comment rédiger** un type de question précis : structure attendue, exemple modèle, pièges et rappels à intégrer.

À lire **en plus** de `redaction_patterns.md` quand tu identifies un type d'exercice listé ici.

## Principe transverse : expliquer la méthode UNE SEULE FOIS par correction

Chaque playbook distingue deux niveaux de rédaction :
- **Version complète** : utilisée la **première fois** qu'un type d'exercice apparaît dans la correction. On explicite le raisonnement (« On sait que … donc il faut … »), on justifie les choix, on rappelle la propriété du cours.
- **Version abrégée** : pour **toutes les occurrences suivantes** du même type dans la même correction. On se contente d'enchaîner les calculs sans redérouler le discours méthodologique.

Règle pratique : dans une correction qui contient 4 comparaisons de fractions, la première est rédigée en version complète, les trois autres en version abrégée. Pareil pour simplifications, additions de fractions, ordres de grandeur, etc.

Si un playbook ne donne qu'une seule version, appliquer ce principe quand même : détailler la première fois, alléger ensuite.

## Index

| Type de question | Fichier | Déclencheurs |
|---|---|---|
| Comparaison de fractions | `comparaison_fractions.md` | « Comparer », « ranger », « classer » des fractions ; `\frac{a}{b}` vs `\frac{c}{d}` avec dénominateurs différents |
| Simplification de fractions | `simplification_fractions.md` | « Simplifier », « réduire », « rendre irréductible » une fraction |
| Addition / soustraction de fractions | `addition_soustraction_fractions.md` | « Calculer », « additionner », « soustraire » `\frac{a}{b} + \frac{c}{d}` ou `-` |
| Décomposition entier + fraction < 1 | `decomposition_entier_fraction.md` | « Décomposer », « écrire sous la forme d'un entier et d'une fraction inférieure à 1 » |
| Produit de fractions | `produit_fractions.md` | « Calculer », « multiplier » `\frac{a}{b} \times \frac{c}{d}` |

## Ajouter un nouveau playbook

1. Créer un fichier `nom_type.md` dans ce dossier.
2. Y décrire : structure attendue, **un exemple rédigé complet**, les pièges, les rappels de cours à mobiliser, quand donner le raisonnement complet vs version abrégée.
3. Ajouter une ligne au tableau d'index ci-dessus avec les déclencheurs (mots-clés ou motifs qui te signalent ce type de question).
