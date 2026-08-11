import pandas as pd
from pathlib import Path


def load_csv(name):
    candidates = [
        Path.cwd() / name,
        Path.cwd() / "my-data" / "raw" / name,
        Path.cwd().parent / "my-data" / "raw" / name,
        Path.cwd() / ".." / "my-data" / "raw" / name,
    ]
    for path in candidates:
        if path.exists():
            return pd.read_csv(path)
    raise FileNotFoundError(f"Could not find {name}")


root_dir = Path.cwd()
if not (root_dir / "my-data").exists():
    root_dir = root_dir.parent

DATA_DIR = root_dir / "my-data" / "raw"
WATCHED_CSV = DATA_DIR / "watched.csv"
LIKES_CSV = DATA_DIR / "likes" / "films.csv"
PROFILE_CSV = DATA_DIR / "profile.csv"

JOIN_KEY = "Letterboxd URI"
FAVORITE_COL = "Favorite Films" 

ratings_df = load_csv("ratings.csv")
watched_df = load_csv("watched.csv")

ratings_df.head(), watched_df.head()


def inspect_columns():

    for label, path in [
        ("watched.csv", WATCHED_CSV),
        ("likes/films.csv", LIKES_CSV),
        ("profile.csv", PROFILE_CSV),
    ]:
        df = pd.read_csv(path)
        print(f"\n{label} columns:")
        print(list(df.columns))
        print(df.head(2))

def load_letterboxd_data():
    watched_df = pd.read_csv(WATCHED_CSV)
    likes_df = pd.read_csv(LIKES_CSV)
    profile_df = pd.read_csv(PROFILE_CSV)
    return watched_df, likes_df, profile_df