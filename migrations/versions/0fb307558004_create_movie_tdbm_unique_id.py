"""create movie tdbm unique id

Revision ID: 0fb307558004
Revises: 275df6e13543
Create Date: 2026-11-08 15:51:13.763382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fb307558004'
down_revision: Union[str, Sequence[str], None] = '275df6e13543'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "movies_title_key",
        "movies",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_movies_tmdb_id",
        "movies",
        ["tmdb_id"],
    )

def downgrade() -> None:
    op.drop_constraint(
        "uq_movies_tmdb_id",
        "movies",
        type_="unique",
    )
    op.create_unique_constraint(
        "movies_title_key",
        "movies",
        ["title"],
    )