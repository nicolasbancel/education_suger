# Playbook — Décomposition d'une fraction sous la forme « entier + fraction < 1 »

## Quand utiliser ce playbook

Toute question qui demande de :
- **décomposer** une fraction sous la forme d'un entier et d'une fraction inférieure à 1
- **écrire** une fraction sous la forme d'un nombre entier plus une fraction
- transformer `\frac{11}{4}` en quelque chose du type `2 + \frac{3}{4}`

Typiquement quand la fraction est **supérieure à 1** (numérateur > dénominateur).

## Méthode

1. **Écrire le numérateur comme une somme** : « plus grand multiple du dénominateur qui tient dans le numérateur » + « reste ».
2. **Séparer en deux fractions** à l'aide de cette somme.
3. **Simplifier** la fraction entière (celle du multiple) : elle donne l'entier.
4. **Conclure** en écrivant la forme finale.

**Important** : il faut choisir le multiple du dénominateur **le plus grand possible** parmi ceux qui restent inférieurs ou égaux au numérateur. Sinon la fraction restante ne sera pas inférieure à 1 et la décomposition n'est pas terminée.

## Exemple rédigé de référence

```latex
\begin{solution}
Pour décomposer une fraction sous la forme d'un entier et d'une fraction
inférieure à 1, on écrit le numérateur comme la somme du plus grand
multiple du dénominateur et du reste, puis on sépare en deux fractions.

Ici, le dénominateur est $4$. Le plus grand multiple de $4$ inférieur ou
égal à $11$ est $8$. On écrit donc $11 = 8 + 3$ :
\[
\frac{11}{4} = \frac{8 + 3}{4} = \frac{8}{4} + \frac{3}{4} = 2 + \frac{3}{4}
\]
\end{solution}
```

## Version abrégée (occurrences suivantes)

Une fois que la méthode a été exposée une fois dans la correction, on se contente d'enchaîner les égalités sans redérouler le discours :

```latex
\[
\frac{17}{5} = \frac{15 + 2}{5} = \frac{15}{5} + \frac{2}{5} = 3 + \frac{2}{5}
\]
```

## Pourquoi le multiple doit être le plus grand possible

Si on choisit un multiple plus petit, la « fraction restante » reste supérieure à 1 et la décomposition n'est pas finie. Exemple à éviter :
```latex
\frac{11}{4} = \frac{4 + 7}{4} = 1 + \frac{7}{4}   % INCORRECT : 7/4 > 1
```
Il faudrait recommencer la décomposition sur `7/4`. D'où la règle : prendre le plus grand multiple du dénominateur qui tient dans le numérateur.

Ce point mérite d'être souligné (en rouge gras ou dans une boîte `Indication`) lors de la première explication de la méthode dans une correction.

## Points de vigilance

- **Vérifier que la fraction restante est bien inférieure à 1** : son numérateur doit être strictement inférieur au dénominateur.
- **Toujours laisser l'étape intermédiaire `\frac{8 + 3}{4}`** visible : c'est là qu'on voit la décomposition à l'œuvre. Ne pas passer directement à `\frac{8}{4} + \frac{3}{4}`.
- **Cas particulier** : si le numérateur est déjà un multiple du dénominateur, la décomposition donne directement un entier (par exemple `\frac{12}{4} = 3`) — pas besoin de décomposition.
- **Cas où la fraction est déjà < 1** : aucune décomposition n'est possible sous cette forme. Le signaler.

## Rappels de cours à mobiliser

- « Pour additionner deux fractions de même dénominateur, on additionne les numérateurs et on garde le dénominateur commun. » (on utilise la propriété **dans l'autre sens** pour séparer une fraction en deux)
- « Une fraction est égale à un entier quand son numérateur est un multiple de son dénominateur. »
