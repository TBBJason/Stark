import tmdbsimple as tmdb
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
tmdb.API_KEY = TMDB_API_KEY



import requests

tmdb.REQUESTS_SESSION = requests.Session()

discover = tmdb.Discover()

response = discover.movie(
    primary_release_date_gte="2026-01-01",
    primary_release_date_lte="2026-12-31",
    sort_by="primary_release_date.asc",
    include_adult=False,
    include_video=False,
    language="en-US",
    page=1,
)


