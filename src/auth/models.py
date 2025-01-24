import uuid
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.books.models import Book

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg




class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = False
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: list["Book"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self):
        return f"<User {self.username}>"
