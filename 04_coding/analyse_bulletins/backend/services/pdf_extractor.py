"""
Extraction de texte depuis les bulletins PDF EcoleDirecte.
Stratégie : pdfplumber en premier (meilleur sur PDF vectoriels),
fallback sur PyMuPDF si pdfplumber retourne trop peu de texte.
"""
import pdfplumber
import fitz  # PyMuPDF
from pathlib import Path


MIN_TEXT_LENGTH = 100  # seuil en dessous duquel on considère l'extraction comme échouée


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrait le texte brut d'un bulletin PDF.
    Retourne une chaîne vide si l'extraction échoue (PDF scanné, corrompu, etc.).
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF introuvable : {pdf_path}")

    # Tentative 1 : pdfplumber
    try:
        text = _extract_with_pdfplumber(pdf_path)
        if len(text.strip()) >= MIN_TEXT_LENGTH:
            return text
    except Exception:
        pass

    # Tentative 2 : PyMuPDF (fallback)
    try:
        text = _extract_with_pymupdf(pdf_path)
        if len(text.strip()) >= MIN_TEXT_LENGTH:
            return text
    except Exception:
        pass

    return ""


def _extract_with_pdfplumber(pdf_path: str) -> str:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def _extract_with_pymupdf(pdf_path: str) -> str:
    pages = []
    doc = fitz.open(pdf_path)
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n\n".join(pages)
