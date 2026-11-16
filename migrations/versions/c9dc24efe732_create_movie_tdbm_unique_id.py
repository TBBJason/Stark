"""create movie tdbm unique id

Revision ID: c9dc24efe732
Revises: 0fb307558004
Create Date: 2026-11-08 15:55:55.856248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9dc24efe732'
down_revision: Union[str, Sequence[str], None] = '0fb307558004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.drop_constraint(
    #     "movies_title_key",
    #     "movies",
    #     type_="unique",
    # )
    # op.create_unique_constraint(
    #     "uq_movies_tmdb_id",
    #     "movies",
    #     ["tmdb_id"],
    # )
    pass

def downgrade() -> None:
    # op.drop_constraint(
    #     "uq_movies_tmdb_id",
    #     "movies",
    #     type_="unique",
    # )
    # op.create_unique_constraint(
    #     "movies_title_key",
    #     "movies",
    #     ["title"],
    pass
    # )