import tmdbsimple as tmdb
import os
from dotenv import load_dotenv
from typing import Any
from pprint import pprint
from normalize_data import normalize_movies
from collections.abc import Iterator
from app.database import SessionLocal
from app.repositories.movies import upsert_movies
from normalize_data import (
    normalize_genres,
    normalize_movies,
)
from app.repositories.genres import (
    replace_movie_genres,
    upsert_genres,
)

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
    page = 1

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

def fetch_movie_genres() -> list[dict[str,Any]]:
    response = tmdb.Genres().movie_list(
        language="en-US",
    )


    return response.get("genres", [])


if __name__ == "__main__":
    raw_genres = fetch_movie_genres()
    normalized_genres = normalize_genres(raw_genres)

    with SessionLocal.begin() as session:
        local_genre_ids_by_tmdb_id = upsert_genres(
            session=session,
            genres=normalized_genres,
        )

    print(
        f"{len(normalized_genres)} genres processed"
    )

    total_processed = 0
    for i in range(2015, 2022):
        for response in fetch_movie_pages(
            year=i,
            max_pages=10,
        ):
            raw_movies = response.get("results", [])
            normalized_records = normalize_movies(raw_movies)

            movie_rows = [
                record["movie"]
                for record in normalized_records
            ]

            movie_genres_by_tmdb_id = {
                record["movie"]["tmdb_id"]: record["genre_ids"]
                for record in normalized_records
            }

            with SessionLocal.begin() as session:
                local_movie_ids_by_tmdb_id = upsert_movies(
                    session=session,
                    movies=movie_rows,
                )

                replace_movie_genres(
                    session=session,
                    movie_genres_by_tmdb_id=movie_genres_by_tmdb_id,
                    local_movie_ids_by_tmdb_id=(
                        local_movie_ids_by_tmdb_id
                    ),
                    local_genre_ids_by_tmdb_id=(
                        local_genre_ids_by_tmdb_id
                    ),
                )

            total_processed += len(movie_rows)

            print(
                f"Page {response['page']}: "
                f"{len(movie_rows)} movies processed"
            )

    print(
        f"\nTotal movies processed: "
        f"{total_processed}"
    )
