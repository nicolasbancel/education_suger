
## Retranscription d'un énoncé

Retranscris moi les énoncés des exercices qui figurent dans l'image en pièce jointe.
Quelques contraintes importantes : 
- Je ne veux pas que tu escap les accents français. N'écris pas "Ar\^ome" mais "Arôme", ni "r\'eaction chimique" mais "réaction chimique"
- Je veux que les formules d'équations chimiques, d'atomes, ou de molécules soient écrits avec la librairie \ce
- Les valeurs et unités doivent être écrites avec la librairie \SI


## Solution et décomposition des raisonnements

<structure>
Le format de sortie doit être du code LaTex

Je veux que chaque raisonnement dans lequel une formule et une application numérique intervient soit décomposé comme suit :
1. Raisonnement. C'est là que tu arrives à la formule finale. Le titre de cette section doit être en couleur : \textcolor{orange}{Raisonnement}
2. Application numérique. C'est là que tu listes les données, les convertis, et exécute l'application numérique. Tu retournes le résultat en notation scientifique et en conservant le bon nombre de chiffres significatifs. Le titre de cette section doit être en couleur : \textcolor{orange}{Application numérique}
3. Interprétation. Tu donnes le résultat de l'application numérique avec une phrase en Français, et si possible, tu en donnes une interprétation. Le titre de cette section doit être en couleur : \textcolor{orange}{Conclusion / Interprétation}
</structure>

<tâche>

Ecris la correction des exercices listés entre les balises <enonces>

Je veux que tu gardes la structure initiale :
- si l'énoncé est sous forme écrite, tu gardes l'énoncé. Et tu écris les réponses entre les questions
- Si l'énoncé est une image : tu écris les réponses en dessous des images en prenant soin de préciser les numéros des questions.

Toutes les réponses doivent être justifiées

Je t'ai donné un exemple d'exercice correctement corrigé entre les balises <exemple_exercice_1>

</tâche>

Voici quelques exemples de corrections bien rédigées 

<exemple_exercice_1>

\textbf{Enoncé}

L'arôme de banane est obtenu en mélangeant \SI{10}{\milli\litre} d'alcool isoamylique (noté \og ai\fg) et \SI{10}{\milli\litre} d'acide éthanoïque (noté \og ae\fg). On obtient aussi de l'eau.

\begin{enumerate}
    \item \textbf{Écrire l'équation de réaction chimique en toutes lettres.}

    \item \textbf{Quelle sera la masse de l'ensemble (hors verrerie) après la transformation chimique ?} \\On donne les masses volumiques suivantes :
    \begin{itemize}
        \item $\rho_{ai} = \SI{0.81}{\gram\per\milli\litre}$
        \item $\rho_{ae} = \SI{1.05}{\gram\per\milli\litre}$
    \end{itemize}
\end{enumerate}

\textbf{Correction}


\begin{enumerate}[label=\textbf{\arabic*.}]
    \item \textbf{Équation de réaction en toutes lettres}\\
    Lorsqu'on mélange de l'alcool isoamylique (ai) et de l'acide éthanoïque (ae), on obtient de l'arôme de banane et de l'eau. La réaction est :
    \[
    \text{alcool isoamylique} + \text{acide éthanoïque} \rightarrow \text{arôme de banane} + \text{eau}
    \]

    \item \textbf{Calcul de la masse après la transformation chimique}\\
    
    \textcolor{orange}{\textbf{Raisonnement}}

    On appelle $m_{ai}$ la masse d'alcool isoamylique \\
    On appelle $m_{ae}$ la masse d'acide éthanoïque \\
    La masse totale des réactifs est notée $m_{totale\_reactifs}$ \\

    On peut écrire que 
    
    \[
    m_{totale\_reactifs} = m_{ai} + m_{ae}
    \]

    En appliquant les formules de la masse volumique, on sait que, avec
    \begin{itemize}[noitemsep]
      \item $V_{ai}$ : Volume d'alcool isoamylique
      \item $\rho_{ai}$ : masse volumique de l'alcool isoamylique
      \item $V_{ae}$ : Volume d'acide éthanoïque
      \item $\rho_{ae}$ : masse volumique de l'acide éthanoïque
    \end{itemize}
    
    \begin{align*}
      m_{ai} &= V_{ai} \times \rho_{ai} \\
      m_{ae} &= V_{ae} \times \rho_{ae} \\
      \intertext{donc} \\
      m_{totale\_reactifs} &= V_{ai} \times \rho_{ai} + V_{ae} \times \rho_{ae}
    \end{align*}
    
    \textcolor{orange}{\textbf{Application numérique}}

    Données :
    \begin{itemize}
        \item Volume d'alcool isoamylique $V_{ai} = 10$ mL et masse volumique $\rho_{ai} = 0.81$ g/mL
        \item Volume d'acide éthanoïque $V_{ae} = 10$ mL et masse volumique $\rho_{ae} = 1.05$ g/mL
    \end{itemize}

    Calcul des masses :
    \[
    m_{ai} = V_{ai} \times \rho_{ai} = 10 \times 0.81 = 8.1 \, \text{g}
    \]
    \[
    m_{ae} = V_{ae} \times \rho_{ae} = 10 \times 1.05 = 10.5 \, \text{g}
    \]
    \[
    m_{totale\_reactifs} = m_{ai} + m_{ae} = 8.1 + 10.5 = 18.6 \, \text{g}
    \]
  
  \textcolor{orange}{\textbf{Conclusion / Interprétation}} \\
  On vient de calculer la masse des réactifs, \textbf{pas celle des produits}. Mais selon la loi de conservation de la masse, on sait que ces deux masses sont égales, donc la masse totale des produits sera également de 18,6 g.

\end{enumerate}

</exemple_exercice_1>

<enonces>



</enonces>


