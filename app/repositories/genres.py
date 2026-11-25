from typing import Any

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import Genre, MovieGenre

def upsert_genres(
    session: Session,
    genres: list[dict[str, Any]],
) -> dict[int, int]:
    if not genres:
        return {}

    insert_statement = insert(Genre).values(genres)

    upsert_statement = (
        insert_statement
        .on_conflict_do_update(
            index_elements=[Genre.tmdb_id],
            set_={
                "name": insert_statement.excluded.name,
            },
        )
        .returning(
            Genre.tmdb_id,
            Genre.id,
        )
    )

    result = session.execute(upsert_statement)

    return dict(result.all())


def replace_movie_genres(
    session: Session,
    movie_genres_by_tmdb_id: dict[int, list[int]],
    local_movie_ids_by_tmdb_id: dict[int, int],
    local_genre_ids_by_tmdb_id: dict[int, int],
) -> None:
    if not movie_genres_by_tmdb_id:
        return

    missing_movie_ids = (
        set(movie_genres_by_tmdb_id)
        - set(local_movie_ids_by_tmdb_id)
    )

    if missing_movie_ids:
        raise ValueError(
            "Movies were not found after upsert: "
            f"{sorted(missing_movie_ids)}"
        )

    referenced_genre_ids = {
        genre_tmdb_id
        for genre_tmdb_ids in movie_genres_by_tmdb_id.values()
        for genre_tmdb_id in genre_tmdb_ids
    }

    missing_genre_ids = (
        referenced_genre_ids
        - set(local_genre_ids_by_tmdb_id)
    )

    if missing_genre_ids:
        raise ValueError(
            "Unknown TMDB genre IDs: "
            f"{sorted(missing_genre_ids)}"
        )

    local_movie_ids = [
        local_movie_ids_by_tmdb_id[movie_tmdb_id]
        for movie_tmdb_id in movie_genres_by_tmdb_id
    ]

    links = {
        (
            local_movie_ids_by_tmdb_id[movie_tmdb_id],
            local_genre_ids_by_tmdb_id[genre_tmdb_id],
        )
        for movie_tmdb_id, genre_tmdb_ids
        in movie_genres_by_tmdb_id.items()
        for genre_tmdb_id in genre_tmdb_ids
    }

    session.execute(
        delete(MovieGenre).where(
            MovieGenre.movie_id.in_(local_movie_ids)
        )
    )

    if links:
        link_rows = [
            {
                "movie_id": movie_id,
                "genre_id": genre_id,
            }
            for movie_id, genre_id in links
        ]

        session.execute(
            insert(MovieGenre).values(link_rows)
        )
