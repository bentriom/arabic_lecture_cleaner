import argparse

from arabic_lecture_cleaner.cleaner import Cleaner
from arabic_lecture_cleaner.constants import LLM_APIS


def main(data_dir: str, api: str, model: str):
    cleaner = Cleaner(data_dir=data_dir)
    cleaner.run(api=api, model=model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="arabic-lecture-cleaner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--api",
        required=False,
        default="ollama",
        type=str,
        help=f"Operating LLM api {LLM_APIS}",
        choices=LLM_APIS,
    )
    parser.add_argument(
        "--model",
        required=False,
        default="mistral-small3.2:24b",
        type=str,
        help="Model identifier (depends on the LLM API).",
    )
    parser.add_argument(
        "--data_dir",
        required=False,
        default="./data",
        type=str,
        help="Directory where the PDF courses are stored.",
    )
    args = parser.parse_args()

    main(data_dir=args.data_dir, api=args.api, model=args.model)
