##This is for OMDb data
import json
import os
import time
from pathlib import Path

import pandas as pd
import requests

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

omdb_url = "http://www.omdbapi.com/"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CACHE_PATH = PROJECT_ROOT / "my-data" / "processed" / "omdb_cache.json"
COMBINED_CSV = PROJECT_ROOT / "my-data" / "processed" / "combined_letterboxd_data.csv"
request_delay = 0.2

def load_cache(): 
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_cache(cache):
    CACHE_PATH.parent.mkdir(parents = True, exist_ok = True)
    with open(CACHE_PATH, "w", encoding = "utf-8") as f:
            json.dump(cache, f, indent = 2)

def _cache_key(title:str, year):
     return f"{title.strip()}_{year}" if pd.notna(year) else title.strip()


def fetch_one(title:str, year, apikey:str):
    params = {"apikey": apikey, "t": title, "type": "movie"}
    if pd.notna(year):
         params["y"] = (int(year))
    try:
         response = requests.get(omdb_url, params=params, timeout= 10)
         response.raise_for_status()
         return response.json()
    except requests.exceptions.RequestException as e:
         return {"Error": f"Request failed: {e}"}

def fetch_all(films_df: pd.DataFrame, apikey:str, title_col = "Name", year_col = "Year"):
    cache = load_cache()
    new_calls = 0

    for _, row in films_df.iterrows():
        key = _cache_key(row[title_col], row[year_col])
        if key in cache: 
            continue
        cache[key] = fetch_one(row[title_col], row[year_col], apikey)
        new_calls += 1
        time.sleep(request_delay)

        if new_calls % 50 == 0:
            _save_cache(cache)
            print(f"... {new_calls} new lookups so far")

    _save_cache(cache)
    print(f"Done! {new_calls} new API calls, {len(cache)} total entries in cache.")
    return cache

def cache_to_dataframe(cache:dict) -> pd.DataFrame:
    records = []
    for key, data in cache.items():
         if data.get("Response") != "True":
              continue
         records.append({
              "cache_key": key,
              "imdbID": data.get("imdbID"), 
              "Title": data.get("Title"),
              "Year": data.get("Year"),
              "Genre": data.get("Genre"),
              "Director": data.get("Director"),
              "Actors": data.get("Actors"),
              "Runtime": data.get("Runtime"),
              "Rated": data.get("Rated"),
              "imdbRating": data.get("imdbRating"),
              "Metascore": data.get("Metascore"),
              "BoxOffice": data.get("BoxOffice"),
              "Country": data.get("Country"),
              "Language": data.get("Language"),
         })
    return pd.DataFrame.from_records(records)

if __name__ == "__main__":
    apikey = os.environ.get("OMDB_API_KEY")
    if not apikey:
         raise EnvironmentError("OMDB_API_KEY environment variable not set. Please set before running script.")
    films_df = pd.read_csv(COMBINED_CSV)[["Name", "Year"]].drop_duplicates()
    cache = fetch_all(films_df, apikey)
    metadata_df = cache_to_dataframe(cache)
    metadata_df.to_csv("my-data/processed/omdb_metadata.csv", index =False)

    missing = len(films_df) - len(metadata_df)
    if missing:
         print(f"Note: {missing} films had no successful OMDb metadata retrieval. Need to give manual search")

     
