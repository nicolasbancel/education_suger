from pathlib import Path


def prompt_get_exercices(file_path=None) -> str:
    base_dir = Path("prompts/template").resolve()

    # Charger le template principal
    with open(base_dir / "latex_prompt_template.md", "r", encoding="utf-8") as f:
        template = f.read()

    # Charger le contenu de la tâche
    with open(
        base_dir / "latex_tache_extraction_exercices.md", "r", encoding="utf-8"
    ) as f:
        tache = f.read()

    # Charger le contenu LaTeX à analyser
    if file_path is None:
        raise ValueError("Le chemin vers le fichier LaTeX doit être fourni.")
    with open(file_path, "r", encoding="utf-8") as f:
        contenu_latex = f.read()

    # Remplacement des placeholders
    prompt = template.replace("[[TACHE]]", tache).replace("[[CONTENU]]", contenu_latex)

    return prompt
