from pathlib import Path

import pdfplumber


def extract_text_from_pdf(pdf_path: Path | str):
    """
    Extracts the text from a PDF file with pdfplumber.

    Args:
        pdf_path (Path | str): Chemin vers le fichier PDF

    Returns:
        str: Texte extrait du PDF

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        Exception: Pour toute autre erreur lors de l'extraction
    """

    pdf_path = Path(pdf_path)
    if not Path(pdf_path).is_file():
        raise FileNotFoundError(f"{pdf_path} is not a file.")

    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for _, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:  # Checks that it has text
                text += page_text + "\n\n"  # Page separator

    return text.strip()  # Supprimer les espaces en début/fin
