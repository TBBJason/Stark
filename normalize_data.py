from datetime import date
from typing import Any

def normalize_movie(movie: dict[str, Any]) -> dict[str, Any]:
    release_date = movie.get("release_date")

    return {
        "tmdb_id": int(movie["id"]),
        "title": movie["title"],
        "release_date": (
            date.fromisoformat(release_date)
            if release_date
            else None),
        "overview": movie.get("overview") or None
    }

def normalize_movies(movies: list[dict[str, Any]],) -> list[dict[str, Any]]:
    return [
        normalize_movie(movie)
        for movie in movies
    ]