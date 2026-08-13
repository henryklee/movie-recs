import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

print(os.environ.get("OMDB_API_KEY"))