# Patterns de rédaction pédagogique — corrections 6ème

Comment rédiger une correction qui ressemble à celles de Nicolas Bancel. Extrait de l'analyse des interros 2 à 5.

## 1. Structure d'une justification : « On sait que / Or / Donc »

Dès qu'une question demande une justification (questions marquées `\justifier` ou `[Justifier]`), structurer la réponse en triplets :

> **On sait que** ... (hypothèse tirée de l'énoncé ou du codage de la figure)
> **Or** ... (propriété du cours mobilisée, énoncée en toutes lettres)
> **Donc** ... (conclusion appliquée au cas particulier)

Puis on passe à l'étape suivante et on enchaîne un nouveau triplet. Ne jamais fondre tout en une seule phrase.

**Exemple typique (interro_5)** :
```
On sait que le polygône DEF a pour symétrique par rapport à la droite (d)
le polygône D'E'F'. L'angle E'D'F' est donc l'image de l'angle EDF par la
symétrie axiale d'axe (d).
Or la symétrie axiale conserve les angles.
Donc E'D'F' = EDF = 60,81°.
```

Variantes acceptables :
- Le « Or » peut être implicite si la propriété est évidente.
- Pour les conclusions immédiates (lecture directe du codage), on peut se contenter de « Sur la figure, ... donc ... ».

## 2. Traitement des questions Vrai/Faux à justifier

Ordre strict :
1. **Réponse immédiate** en gras rouge : `\textbf{\textcolor{red}{[VRAI]}}` ou `[FAUX]`.
2. **Observation** : « Sur la figure, … » ou « D'après le codage, … ».
3. **Démonstration** (texte ou `align*`).
4. **Conclusion réaffirmée** en gras : `\textbf{L'affirmation est vraie.}` / `\textbf{L'affirmation est fausse.}`.

**Bonus pédagogique** : pour les exercices avec beaucoup de VF, donner d'abord un *résumé* des réponses attendues dans un `compactparts`, avant de détailler question par question (vu dans interro_3 exercice 3).

## 3. Hypothèses : toujours ancrées dans l'énoncé ou la figure

Commencer systématiquement par rendre visible d'où vient l'information :
- « **Sur la figure**, les segments [AB], [BC], [CD] et [DE] sont de même longueur. »
- « **D'après le codage**, AG = GE. »
- « **D'après l'énoncé**, le triangle est isocèle en A. »
- « **On observe que** les trois côtés portent le même codage : le triangle est donc équilatéral. »

Jamais d'hypothèse cachée.

## 4. Rappels de cours intégrés

Les propriétés mobilisées sont **toujours énoncées en toutes lettres** avant d'être appliquées, typiquement en gras.

**Exemple (interro_4)** :
```
D'après le cours, on sait que chaque angle d'un triangle équilatéral
mesure 60°. Ainsi, AEF = 60°.
```

Puis l'application suit immédiatement, souvent dans un `align*`.

Pour un exercice qui mobilise une notion centrale (commutativité, priorités opératoires, conservation par symétrie…), ne pas hésiter à faire un **encart de rappel** en début de correction, façon « avant de commencer, rappelons deux propriétés importantes ».

## 5. Exposer la stratégie avant les exercices complexes

Pour les problèmes difficiles, **expliquer le plan** en rouge gras (`\textrr{...}`) avant d'attaquer la résolution. Exemple d'ouverture type :

> « Les points H, A, P sont alignés : l'angle HAP est donc un angle plat, il vaut 180°. L'enjeu de l'exercice étant de trouver la mesure de l'angle CAT, on va chercher à calculer les angles HAC et TAP, puis en déduire la mesure de CAT. Enfin, on pourra conclure si le triangle CAT est rectangle en A ou non. »

Puis on suit ce plan étape par étape, en réutilisant les mêmes termes pour que l'élève puisse se repérer.

## 6. Erreurs courantes : les signaler, expliquer POURQUOI elles sont fausses

Pattern fréquent : en rouge gras, montrer la rédaction fautive, puis expliquer ce qui cloche.

**Exemple (interro_3 exercice 5)** :
> « Une erreur que je vois encore trop souvent est que vous faites :
> A = (9+1) = 10, A = (14-3) = 11, A = 10 × 11 = 110.
> C'est faux : ici, vous donnez 3 valeurs différentes à A. Vous dites alternativement qu'il vaut 10, puis 11, puis 110. La seule rédaction correcte est celle où vous intégrez vos calculs intermédiaires dans le calcul global. »

À faire dans un bloc séparé (souvent un second `\begin{solution}` après la réponse, ou une boîte `Indication`).

## 7. Présentation de plusieurs méthodes

Pour les questions de construction géométrique ou de calcul astucieux, montrer **2 méthodes** quand elles sont didactiquement utiles :
```latex
\begin{itemize}
  \item \textbf{Méthode au compas} : ...
  \item \textbf{Méthode à la règle graduée et à l'équerre} : ...
\end{itemize}
```
Nommer clairement chaque méthode en gras en début d'item.

Pour un résultat connu du cours (ex. angles d'un équilatéral), donner **le résultat immédiat** (« on sait que ... = 60° »), puis proposer **la re-démonstration** en bonus (« On peut facilement retrouver ce résultat : ... »).

## 8. Ton général

- **« On »** partout. Pas de tutoiement, pas de « nous », pas de « vous » sauf dans les adresses directes en rouge gras (« vous devez », « je vous rappelle »).
- Ton **formel mais accessible**, **bienveillant**. Préférer « ce qui était attendu » à « vous avez oublié ».
- Didactique : expliquer la stratégie, pas uniquement dérouler les calculs.
- Humour doux et très rare, jamais cruel (« une approximation absurde »).

## 8bis. Principe « une explication par correction »

Quand plusieurs questions du même type s'enchaînent (plusieurs comparaisons de fractions, plusieurs ordres de grandeur, plusieurs additions de fractions…), **expliquer la méthode UNE SEULE fois** — typiquement à la première occurrence — puis passer en version abrégée pour toutes les suivantes.

Voir `playbooks/README.md` (section « Principe transverse ») pour le détail. Chaque playbook précise la forme de ses versions complète et abrégée.

## 9. Niveau de détail : adapter au type de question

| Type de question | Verbosité |
|---|---|
| Réponse factuelle (écrire en lettres, donner un chiffre) | Très courte, 1 ligne. |
| Calcul simple | `align*` de 4-5 lignes, commentaires courts sur chaque étape. |
| Calcul complexe / priorités | `align*` complet + mise en garde séparée sur les erreurs fréquentes. |
| Construction géométrique | `compactenum` des étapes principales (pas de détail sur la manipulation des outils) + vérification finale (« Sur la figure, on vérifie que AB = 7 cm… ») + figure. |
| Justification géométrique | Triptyque « On sait / Or / Donc », ancré dans le codage. |
| Question de cours (définition) | Une phrase précise, vocabulaire strict, éléments clés en gras. Éventuellement « Autrement dit, … » en reformulation. |
| Problème ouvert / exercice piégé | Stratégie en rouge gras d'abord, puis résolution pas à pas. |

## 10. Conclusion d'une question

Toujours **visible et isolée**, typiquement en gras :
- `\textbf{L'affirmation est vraie.}`
- `\textbf{Conclusion :} le triangle CAT n'est pas rectangle en A car CAT = 88° ≠ 90°.`
- `\textbf{L'affirmation est vraie : C est le milieu de [AE].}`

Jamais une conclusion noyée au milieu d'un paragraphe.

## 11. Vérifications finales

Pour les constructions, ajouter une **vérification** après la procédure :
> « Sur la figure, on vérifie que AB = 7 cm, AC = 8,5 cm et BC = 10 cm. »

C'est à la fois un rappel méthodologique (l'élève doit le faire aussi) et une preuve que la construction est correcte.

## 12. Connecteurs logiques utilisés

Fréquents : **On sait que**, **Or**, **Donc**, **Ainsi**, **Autrement dit**, **D'après le cours**, **Sur la figure**, **On observe que**, **On a donc**, **Il suffit donc de**.

À utiliser avec parcimonie : « Cependant », « Néanmoins ».

Éviter : « Du coup », « Alors » (trop oral).

## 13. Références croisées

Autoriser et encourager : « d'après la question a) », « on a trouvé précédemment que … », « on réutilise le résultat de la question b) ». Cela apprend aux élèves à chaîner leurs raisonnements.
