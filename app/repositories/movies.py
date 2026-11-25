from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import Movie

def upsert_movies(
    session: Session,
    movies: list[dict[str, Any]],
) -> dict[int,int]:
    if not movies:
        return

    insert_statement = insert(Movie).values(movies)

    upsert_statement = (
        insert_statement.on_conflict_do_update(
            constraint="uq_movies_tmdb_id",
            set_={
                "title": insert_statement.excluded.title,
                "release_date": insert_statement.excluded.release_date,
                "overview": insert_statement.excluded.overview,
            },
        ).returning (
            Movie.tmdb_id,
            Movie.id,
        )
    )

    result = session.execute(upsert_statement)

    return dict(result.all())
