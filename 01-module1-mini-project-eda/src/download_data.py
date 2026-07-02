"""Download the Titanic passenger dataset used by this project.

Run this once from the project root:
    python src/download_data.py
"""
import pathlib
import urllib.request

URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
DEST = pathlib.Path(__file__).resolve().parent.parent / "data" / "titanic.csv"


def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(URL, DEST)
    print(f"Saved dataset to {DEST}")


if __name__ == "__main__":
    main()
