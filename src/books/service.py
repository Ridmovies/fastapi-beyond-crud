from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.books.models import Book
from src.books.schemas import BookCreateSchema
from src.services import BaseService


class BookService(BaseService):
    model = Book

    @classmethod
    async def create_book(
        cls, book_data: BookCreateSchema, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        # new_book.published_date = datetime.strptime(
        #     book_data_dict["published_date"], "%Y-%m-%d"
        # )

        session.add(new_book)

        await session.commit()

        return new_book
