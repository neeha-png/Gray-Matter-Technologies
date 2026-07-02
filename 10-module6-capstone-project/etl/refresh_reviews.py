"""Minimal ETL step: refreshes the raw review data that the model could be
retrained on.

In a real deployment this would pull from the store's live review feed/API
instead of a static public dataset -- but the *pattern* is the same: pull
new data on a schedule, normalize it, dedupe against what's already been
seen, and land it somewhere the training pipeline can pick up. This script
demonstrates that pattern end-to-end against the same public dataset
project 8 was trained on.

Run it manually:
    python etl/refresh_reviews.py
Or on a schedule -- see .github/workflows/ci.yml's nightly cron job.
"""
import hashlib
import pathlib
import urllib.request
import zipfile

import pandas as pd

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
INCOMING_DIR = PROJECT_ROOT / "data" / "incoming"
SEEN_HASHES_PATH = INCOMING_DIR / "seen_hashes.txt"
SOURCE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00331/sentiment%20labelled%20sentences.zip"


def download_source(dest_dir: pathlib.Path) -> pathlib.Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / "sentiment_sentences.zip"
    urllib.request.urlretrieve(SOURCE_URL, zip_path)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest_dir)
    zip_path.unlink()
    return dest_dir / "sentiment labelled sentences"


def load_all_reviews(extracted_dir: pathlib.Path) -> pd.DataFrame:
    frames = []
    for name, source in [("amazon_cells_labelled.txt", "amazon"),
                          ("yelp_labelled.txt", "yelp"),
                          ("imdb_labelled.txt", "imdb")]:
        df = pd.read_csv(extracted_dir / name, sep="\t", header=None, names=["text", "label"])
        df["source"] = source
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def load_seen_hashes() -> set:
    if not SEEN_HASHES_PATH.exists():
        return set()
    return set(SEEN_HASHES_PATH.read_text().splitlines())


def save_seen_hashes(hashes: set):
    SEEN_HASHES_PATH.write_text("\n".join(sorted(hashes)))


def main():
    extracted_dir = download_source(INCOMING_DIR / "_download")
    reviews = load_all_reviews(extracted_dir)

    reviews["hash"] = reviews["text"].apply(lambda t: hashlib.sha256(t.encode()).hexdigest())
    seen = load_seen_hashes()
    new_reviews = reviews[~reviews["hash"].isin(seen)]

    print(f"Fetched {len(reviews)} reviews from source, {len(new_reviews)} not seen before.")

    if len(new_reviews) > 0:
        snapshot_path = INCOMING_DIR / "latest_batch.csv"
        new_reviews.drop(columns=["hash"]).to_csv(snapshot_path, index=False)
        print(f"Saved new batch -> {snapshot_path}")

        save_seen_hashes(seen | set(reviews["hash"]))
        print(f"Updated seen-hashes store: {len(seen | set(reviews['hash']))} total reviews tracked.")
    else:
        print("No new reviews since last refresh -- nothing to save.")


if __name__ == "__main__":
    main()
