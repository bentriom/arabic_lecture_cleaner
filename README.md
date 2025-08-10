# Arabic Lecture Cleaner

A Python tool for extracting and cleaning Arabic text from PDF lecture documents using Large Language Models (LLMs). This tool processes PDF files by extracting their textual content and then applies LLM-based cleaning to improve readability and structure.

## Features

- **PDF Text Extraction**: Automatically extracts text from PDF lecture files
- **LLM-based Cleaning**: Uses state-of-the-art language models to clean and structure extracted text
- **Flexible Deployment**: Supports both local (Ollama) and API-based LLM inference
- **Batch Processing**: Processes multiple PDF files in a single run
- **Organized Output**: Saves extraction and cleaning results in structured directories

## Installation

```bash
git clone https://github.com/bentriom/arabic-lecture-cleaner.git
```

And use your favorite environment manager to install dependencies (the project was initialized with `uv`).

## Prerequisites

### For Local Mode (Ollama)
- Install [Ollama](https://ollama.ai/)
- Pull your desired model: `ollama pull mistral-small3.2:24b`

### For API Mode
- Ensure you have access to the Mammouth AI API
- Configure your API credentials (details in configuration section)

## Usage

### Command Line Interface

```bash
python main.py --data_dir ./data --mode local --model mistral-small3.2:24b
```

### Parameters

- `--data_dir`: Directory containing PDF files to process (default: `./data`)
- `--mode`: Processing mode - `local` for Ollama or `api` for external API (default: `local`)  
- `--model`: Model identifier (default: `mistral-small3.2:24b`)

### Examples

**Local processing with Gemma:**
```bash
python main.py --data_dir ./lectures --mode local --model gemma3:27b
```

**API processing:**
```bash
python main.py --data_dir ./course_materials --mode api --model gemini-2.5-flash
```

## Project Structure

```
arabic-lecture-cleaner/
├── arabic_lecture_cleaner/
│   ├── cleaner.py              # Main Cleaner class
│   ├── constants.py            # Prompts and constants
│   ├── llm_cleaning.py         # LLM processing functions  
│   └── pdf_extraction.py       # PDF text extraction utilities
├── main.py                     # CLI entry point
├── data/                       # Input PDF directory (create this)
└── results/                    # Output directory (auto-created)
    ├── extraction/             # Raw extracted text
    └── {mode}/{model}/         # Cleaned text by mode/model
```

## Programmatic Usage

```python
from arabic_lecture_cleaner.cleaner import Cleaner

# Initialize cleaner
cleaner = Cleaner(data_dir="./my_pdfs", results_dir="./output")

# Run complete pipeline
cleaner.run(mode="local", model="gemma3:27b")

# Or run steps individually
cleaner.extract_pdf_texts()
cleaner.clean_with_llm(mode="local", model="gemma3:27b")

# Access results
extracted_texts = cleaner.extracted_pdfs
cleaned_texts = cleaner.cleaned_extracted_pdfs
```

## Output

The tool generates organized output in the `results` directory:

- `results/extraction/`: Raw text extracted from PDFs
- `results/local/{model}/`: Cleaned text using local models
- `results/api/{model}/`: Cleaned text using API models

Each processed file creates corresponding `.txt` files with extracted and cleaned content.

## Supported Models

### Local (Ollama)
- `gemma3:27b` (default fallback)
- `mistral-small3.2:24b` (CLI default)
- Any model available in your local Ollama installation

### API
- Model availability depends on your API provider configuration

## Configuration

To use the API mode, ensure that an environment variable `MAMMOUTH_API_KEY` is set with a [valid API key from Mammouth AI](https://mammouth.ai/app/account/settings/api).

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and add tests
4. Commit: `git commit -am 'Add new feature'`
5. Push: `git push origin feature/new-feature`
6. Submit a Pull Request

## Support

For issues and questions, please open a GitHub issue.
