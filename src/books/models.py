import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.auth.models import User

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel, Column, Relationship




class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )

    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    user_uid: uuid.UUID | None = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    user: Optional["User"] = Relationship(back_populates="books")


