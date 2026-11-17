import tmdbsimple as tmdb
import os
from dotenv import load_dotenv
from typing import Any
from pprint import pprint

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
tmdb.API_KEY = TMDB_API_KEY
tmdb.REQUESTS_TIMEOUT = (3.05, 20)



import requests

def fetch_movie_page(year:int, page:int = 1,) -> dict[str, Any]:


# tmdb.REQUESTS_SESSION = requests.Session()

    discover = tmdb.Discover()

    response = discover.movie(
        primary_release_date_gte=f"{year}-01-01",
        primary_release_date_lte=f"{year}-12-31",
        sort_by="primary_release_date.asc",
        include_adult=False,
        include_video=False,
        language="en-US",
        page=page,
    )
    return response

if __name__ == "__main__":
    response = fetch_movie_page(year=2026, page=1)

    print("\nTop-level fields:")
    print(response.keys())

    print("\nPagination:")
    print(f"Current page: {response['page']}")
    print(f"Total pages: {response['total_pages']}")
    print(f"Total results: {response['total_results']}")
    print(f"Results on this page: {len(response['results'])}")

    if response["results"]:
        first_movie = response["results"][0]

        print("\nAvailable fields for one movie:")
        pprint(sorted(first_movie.keys()))

        print("\nSelected movie data:")
        pprint({
            "id": first_movie.get("id"),
            "title": first_movie.get("title"),
            "release_date": first_movie.get("release_date"),
            "overview": first_movie.get("overview"),
            "genre_ids": first_movie.get("genre_ids"),
        })

