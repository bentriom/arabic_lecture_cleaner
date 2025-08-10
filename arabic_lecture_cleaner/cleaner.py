import os
from pathlib import Path

import ollama
from loguru import logger

import arabic_lecture_cleaner.constants as const
from arabic_lecture_cleaner.llm_cleaning import (
    process_text_local,
    process_text_mammouth_api,
)
from arabic_lecture_cleaner.pdf_extraction import extract_text_from_pdf


class Cleaner:
    """Cleaner for Arabic transcripts.

    Parameters
    ----------
    data_dir : str
        Path to directory containing resources (e.g. tokenizer, dictionaries, etc.).
    mode : str, optional
        Operation mode: ``"local"`` to use local resources,
        ``"api"`` to call an external API. Defaults to ``"local"``.
    """

    def __init__(self, data_dir: str | Path, results_dir: str | Path = "./results"):
        data_dir = Path(data_dir)
        results_dir = Path(results_dir)
        os.makedirs(results_dir, exist_ok=True)
        if not data_dir.is_dir():
            raise ValueError(f"{data_dir} is not a directory.")
        self.data_dir = data_dir
        self.results_dir = results_dir
        self.extracted_pdfs = None
        self.cleaned_extracted_pdfs = None

    def extract_pdf_texts(self):
        self.extracted_pdfs = {}
        results_extract_dir = self.results_dir / "extraction"
        os.makedirs(results_extract_dir, exist_ok=True)
        for file in self.data_dir.glob("*.pdf"):
            extracted_text = extract_text_from_pdf(file)
            self.extracted_pdfs[file.stem] = extracted_text
            save_path = results_extract_dir / f"{file.stem}.txt"
            logger.info(f"Export results to {save_path}")
            with open(save_path, "w") as f:
                f.write(extracted_text)

    def clean_with_llm(self, mode: str, model: str):
        if mode not in {"local", "api"}:
            raise ValueError(f"Invalid mode {mode!r}. Must be 'local' or 'api'.")
        self.cleaned_extracted_pdfs = {}
        results_cleaning_dir = self.results_dir / "local" / model.replace(":", "_")
        os.makedirs(results_cleaning_dir, exist_ok=True)
        for file, text in self.extracted_pdfs.items():
            logger.info(f"Cleaning {file}")
            if mode == "local":
                if model not in [m.model for m in ollama.list().models]:
                    raise ValueError(
                        f"{model} not available in Ollama (models: {ollama.list()}). Please run 'ollama pull {model}'."
                    )
                cleaned_text = process_text_local(const.PREPROMPT_1, text, model)
            elif mode == "api":
                cleaned_text = process_text_mammouth_api(const.PREPROMPT_1, text, model)
            save_path = results_cleaning_dir / f"{file}_cleaned.txt"
            logger.info(f"Export results to {save_path}")
            with open(save_path, "w") as f:
                f.write(cleaned_text)
            self.cleaned_extracted_pdfs[file] = cleaned_text

    def run(self, mode: str = "local", model: str = "gemma3:27b"):
        if mode not in {"local", "api"}:
            raise ValueError(f"Invalid mode {mode!r}. Must be 'local' or 'api'.")
        logger.info(f"Launching cleaner in mode {mode} with LLM model {model}")
        logger.info("Extracting text from pdf")
        self.extract_pdf_texts()
        logger.info("Cleaning with llm")
        self.clean_with_llm(mode=mode, model=model)
