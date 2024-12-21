import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel, Column


class Book(SQLModel, table=True):
    id: int = Field(primary_key=True)
    # __tablename__ = "books"
    # uid: uuid.UUID = Field(
    #     sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    # )

    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))