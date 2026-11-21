from datetime import date
from typing import Any

def normalize_movie(movie: dict[str, Any]) -> dict[str, Any]:
    release_date = movie.get("release_date")

    return {
        "movie": {
            "tmdb_id": int(movie["id"]),
            "title": movie["title"],
            "release_date": (
                date.fromisoformat(release_date)
                if release_date
                else None
            ),
            "overview": movie.get("overview") or None,
        },
        "genre_ids": [
            int(genre_id)
            for genre_id in movie["genre_ids"]
        ],
    }

def normalize_movies(movies: list[dict[str, Any]],) -> list[dict[str, Any]]:
    return [
        normalize_movie(movie)
        for movie in movies
    ]

def normalize_genre(genre:dict[str, Any],) -> dict[str,Any]:
    return {
        "tmdb_id": int(genre["id"]),
        "name":genre["name"],
    }

def normalize_genres(genres:list[dict[str,Any]],) -> list[dict[str,Any]]:
    return [
        normalize_genre(genre)
        for genre in genres
    ]