from fastapi import APIRouter
from sqlmodel import select

from src.books.models import Book
from src.books.service import BookService
from src.database import SessionDep

router = APIRouter()


@router.get("/")
async def get_all_books():
    books = await BookService.get_all()
    return books


# @router.post("/")
# async def create_book(book_data: Book):
#     book = await BookService.create(book_data)
#     return book