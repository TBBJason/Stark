from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class User(Base):
    __table__name = "users"


class Movies(Base):
    __table__name = "movies"

class Ratings(Base):
    __table__name = "ratings"