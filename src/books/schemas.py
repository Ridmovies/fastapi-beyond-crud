import uuid
from datetime import date, datetime

from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime
    update_at: datetime


# class BookDetailModel(Book):
#     reviews: list[ReviewModel]
#     tags:list[TagModel]


class BookCreateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


class BookPatchSchema(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    page_count: int | None = None
    language: str | None = None