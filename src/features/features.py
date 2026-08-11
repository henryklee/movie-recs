import pandas as pd

#Combine the three established letterboxd dataframes into a single dataframe 
#with liked and favorite flags
JOIN_KEY = "Letterboxd URI"
FAVORITE_COL = "Favorite Films"

def combine_letterboxd_data(watched_df, likes_df, profile_df):
    df = watched_df.copy()

    # --- Liked flag ---
    if JOIN_KEY not in likes_df.columns:
        raise KeyError(
            f"'{JOIN_KEY}' not found in likes_df columns: {list(likes_df.columns)}. "
            "Run inspect_columns() to check the actual header names."
        )
    liked_uris = set(likes_df[JOIN_KEY].dropna())
    df["Liked"] = df[JOIN_KEY].isin(liked_uris)

    # --- Favorite flag ---
    if FAVORITE_COL not in profile_df.columns:
        raise KeyError(
            f"'{FAVORITE_COL}' not found in profile_df columns: "
            f"{list(profile_df.columns)}. Run inspect_columns() to check the actual "
            "header names."
        )

    raw = profile_df[FAVORITE_COL].iloc[0]
    favorite_uris = {uri.strip() for uri in raw.split(",")}
    df["Favorite"] = df[JOIN_KEY].isin(favorite_uris)

    return df
