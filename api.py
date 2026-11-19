import tmdbsimple as tmdb
import os
from dotenv import load_dotenv
from typing import Any
from pprint import pprint
from normalize_data import normalize_movies
from collections.abc import Iterator
from app.database import SessionLocal
from app.repositories.movies import upsert_movies

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
        sort_by="popularity.desc",
        include_adult=False,
        include_video=False,
        language="en-US",
        with_original_language="en",
        page=page,
    )
    return response


def fetch_movie_pages(year: int,max_pages: int | None = None,) -> Iterator[dict[str, Any]]:
    page = 6

    while True:
        response = fetch_movie_page(
            year=year,
            page=page,
        )

        yield response

        total_pages = int(response["total_pages"])

        if page >= total_pages:
            break

        if max_pages is not None and page >= max_pages:
            break

        page += 1


if __name__ == "__main__":
    total_processed = 0

    for response in fetch_movie_pages(
        year=2026,
        max_pages=5,
    ):
        raw_movies = response.get("results", [])
        normalized_movies = normalize_movies(raw_movies)

        with SessionLocal.begin() as session:
            upsert_movies(
                session=session,
                movies=normalized_movies,
            )

        total_processed += len(normalized_movies)

        print(
            f"Page {response['page']}: "
            f"{len(normalized_movies)} movies processed"
        )

    print(
        f"\nTotal movies processed: "
        f"{total_processed}"
    )

