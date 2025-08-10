from pathlib import Path

import ollama
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


def process_text_with_instructions(
    instruction_prompt: str, text_to_process: str, model: str
):
    """
    Process text using specific instructions via Ollama.

    Args:
        instruction_prompt: Instructions defining the model's role/behavior
        text_to_process: The actual text to operate on
        model: Ollama model name
    """
    messages = [
        {"role": "system", "content": instruction_prompt},
        {"role": "user", "content": "Traite ce texte: " + text_to_process},
    ]

    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"]
