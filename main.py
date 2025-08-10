from arabic_lecture_cleaner.cleaner import Cleaner


def main():
    cleaner = Cleaner(data_dir="./data")
    cleaner.run()


if __name__ == "__main__":
    main()
