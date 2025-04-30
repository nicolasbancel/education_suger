def create_latex_document(image_path, correction_text, output_path):
    latex_content = r"""\documentclass{article}
\usepackage{graphicx}
\begin{document}

\section*{Exercise}
\begin{figure}[h]
    \centering
    \includegraphics[width=\textwidth]{%s}
    \caption{Cropped Exercise}
\end{figure}

\section*{Correction}
%s

\end{document}
""" % (image_path, correction_text)

    with open(output_path, 'w') as latex_file:
        latex_file.write(latex_content)

def compile_latex(output_path):
    import subprocess
    subprocess.run(['pdflatex', output_path])