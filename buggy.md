
## Example of buggy macros or functions

```latex
\newcommand{\troubugnew}[3]{%
    \ifthenelse{\equal{\WITH_CORRECTION}{NO}}{%
        % If WITH_CORRECTION is NO, insert either vertical or horizontal blank spaces
        \ifthenelse{\equal{#1}{v}}{
            \vspace{#2em} % Vertical blank space 
        }
        {
          \ifthenelse{\equal{#1}{h}}{
            \hspace{#2em} % Horizontal blank space 
          }
          {}
        }%
        %
      }
    {%
        % If WITH_CORRECTION is YES, show the answer
        \ifmmode
        In Maths mode
        % \colorbox{lightgray}{#3}
        \else 
        % We create this if condition because otherwise the colorbox has a very large size 
        % which exceeds the size of other boxes
        %NOT in Maths mode
        \colorbox{lightgray}{#3}
        \fi 
        % hlgray is removed because it does not work well when in Maths mode
        
    }%
}
```
