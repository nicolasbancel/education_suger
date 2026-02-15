## Issue with `declare` function in tikz

- Solved using this [tikz declare function and babel french option](https://tex.stackexchange.com/questions/86023/tikz-declare-function-and-babel-french-option)
- And then removing french from the list of languages : `\RequirePackage[english, french]{babel}` : it was messing up things when a tkiz figure was included in the \ans macro
