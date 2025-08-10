import argparse

from arabic_lecture_cleaner.cleaner import Cleaner


def main(mode: str, model: str):
    cleaner = Cleaner(data_dir="./data")
    cleaner.run(mode=mode, model=model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="arabic-lecture-cleaner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        required=False,
        default="local",
        type=str,
        help="Operating mode ('api' or 'local').",
        choices=["api", "local"],
    )
    parser.add_argument(
        "--model",
        required=False,
        default="mistral-small3.2:24b",
        type=str,
        help="Model identifier (depends on local or API call).",
    )
    args = parser.parse_args()

    main(mode=args.mode, model=args.model)
