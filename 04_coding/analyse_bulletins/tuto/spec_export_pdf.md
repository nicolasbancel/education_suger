# Spécification — Export PDF par élève

## Objectif

Générer un PDF **par élève** résumant son trimestre courant (`trimestre` T_n).
Le PDF est produit par l'endpoint `GET /api/export/{classe_id}/pdf?trimestre={n}` et englobe
l'ensemble des élèves de la classe dans un seul fichier (un bloc par élève, saut de page entre chaque).

---

## Sources de données

| Donnée | Modèle / Champ |
|---|---|
| Identité élève | `Student.first_name`, `Student.last_name` |
| Notes du trimestre courant T_n | `BulletinLine` filtrés sur `student_id` + `trimestre == n` |
| Notes du trimestre précédent T_{n-1} | `BulletinLine` filtrés sur `student_id` + `trimestre == n-1` |
| Bilan PP / mention / VS / CE (T_n et T_{n-1}) | `BulletinLine` avec `subject == "BILAN"` |
| Appréciation LLM | `LLMOutput` filtré sur `student_id` + `trimestre == n` |
| Vie scolaire | `VieScolaireEvent` filtrés sur `student_id` + dates du trimestre (`config.TRIMESTRES_DATES`) |
| Sanctions / encouragements | `SanctionEncouragement` filtrés sur `student_id` + dates du trimestre |

---

## Structure du bloc par élève

### H1 — Prénom Nom

Exemple : `Salomé AMAR`

---

### H2 — Résultats

Tableau des notes par matière.

#### Colonnes du tableau

| Colonne | Source |
|---|---|
| **Matière** | `BulletinLine.subject` (toutes les lignes où `subject != "BILAN"`) |
| **Élève T_n** | `BulletinLine.average` (trimestre n) |
| **Classe T_n** | `BulletinLine.average_class` (trimestre n) |
| **Élève T_{n-1}** | `BulletinLine.average` (trimestre n-1), même `subject` |
| **Δ T_n − T_{n-1}** | `average(T_n) − average(T_{n-1})`, affiché avec signe (+/-) et arrondi à 2 décimales. Cellule avec **gradient de couleur de fond** : négatif → rouge (plus foncé si valeur absolue grande), positif → vert (plus foncé si valeur absolue grande), zéro → neutre. |
| **Appréciation T_n** | `BulletinLine.appreciation` (trimestre n) |
| **Appréciation T_{n-1}** | `BulletinLine.appreciation` (trimestre n-1), même `subject` |

#### Règles de la colonne Δ (gradient)

- Seuils indicatifs pour la saturation de couleur :
  - `|Δ| ≥ 3` → couleur maximale (rouge foncé ou vert foncé)
  - `|Δ| ∈ [1, 3[` → couleur intermédiaire
  - `|Δ| < 1` → couleur faible (quasi-neutre)
- Si `average(T_{n-1})` est `None` (pas de donnée T_{n-1}) → cellule vide, pas de couleur.

#### Dernière ligne — Moyenne générale

Ligne de synthèse construite depuis le `BulletinLine` avec `subject == "BILAN"` :

| Colonne | Source |
|---|---|
| **Matière** | Texte fixe : `"Moyenne générale"` |
| **Élève T_n** | `BulletinLine(subject="BILAN", trimestre=n).average` |
| **Classe T_n** | `BulletinLine(subject="BILAN", trimestre=n).average_class` |
| **Élève T_{n-1}** | `BulletinLine(subject="BILAN", trimestre=n-1).average` |
| **Δ T_n − T_{n-1}** | Idem règle ci-dessus + même gradient de couleur |
| **Appréciation T_n** | — (vide) |
| **Appréciation T_{n-1}** | — (vide) |

La ligne "Moyenne générale" doit être visuellement distinguée (fond gris clair, texte en gras).

---

### H2 — Appréciations

#### H3 — Trimestre précédent (T_{n-1})

Données issues du `BulletinLine(subject="BILAN", trimestre=n-1)` de l'élève.

- **Appréciation du professeur principal** : `BulletinLine.appreciation`
- **Mention du conseil** : `BulletinLine.mention` (si `None` → afficher `"Pas de récompense / mention"`)
- **Appréciation du chef d'établissement** : `BulletinLine.appreciation_ce`

> Si aucun bulletin T_{n-1} n'existe (trimestre 1), cette section est omise.

#### H3 — Ce trimestre (T_n)

##### H4 — Incidents / Vie scolaire

Données issues de `VieScolaireEvent` et `SanctionEncouragement`, filtrés sur les dates de T_n
via `config.TRIMESTRES_DATES[n]`.

- **Absences non justifiées** : `VieScolaireEvent` où `event_type == "absence"` et `justifie == False`.
  Afficher : `display_date` (ou `date`), `libelle`, `motif` si présent.
- **Retards** : `VieScolaireEvent` où `event_type == "retard"`.
  Afficher : `display_date`, `libelle` (durée ex. `"00:15"`), `motif` si présent.
- **Sanctions / Encouragements** : `SanctionEncouragement`.
  Afficher : `display_date`, `type_element`, `libelle`, `motif` si présent.

Si aucun événement → section omise (ne pas afficher le titre H4).

##### H4 — Appréciation générale

Données issues de `LLMOutput` filtré sur `student_id` + `trimestre == n`.

- **Appréciation générale** : `LLMOutput.general_appreciation`
- **Synthèse** : `LLMOutput.synthesis` (affiché tel quel, respect des sauts de ligne)
- **Récompense suggérée** : `LLMOutput.reward_suggestion`

Si aucun `LLMOutput` n'existe pour cet élève → afficher `"Aucune appréciation générée."`.

---

## Mise en page générale

- Format page : **A4 portrait**
- **Saut de page** entre chaque élève
- Police : sans-serif (ex. Helvetica)
- Tailles :
  - H1 (nom élève) : 16 pt, gras
  - H2 : 13 pt, gras
  - H3 : 11 pt, gras, légèrement indenté
  - H4 : 10 pt, gras, italique
  - Corps / tableau : 9 pt
- Tableau des notes :
  - Colonnes **Matière** et **Appréciation** : largeur extensible
  - Colonnes numériques (**Élève**, **Classe**, **Δ**) : largeur fixe étroite, centré
  - Bordures légères (gris clair)
  - En-tête de tableau : fond gris, texte gras

---

## Notes d'implémentation (reportlab)

- Utiliser `platypus.Table` avec `TableStyle` pour les couleurs de cellule du gradient Δ.
- Pour le gradient, calculer la couleur BACKGROUND à la création de chaque ligne via `colors.Color(r, g, b)` de reportlab.
- `Paragraph` avec style `Normal` pour les appréciations longues (gère le retour à la ligne automatique).
- `PageBreak()` entre chaque élève.
- Les champs `None` doivent être remplacés par `"—"` dans le tableau et omis (section entière) dans les blocs texte, sauf `mention` qui affiche `"Pas de récompense / mention"`.
