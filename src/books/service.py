from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from src.books.models import Book
from src.books.schemas import BookCreateSchema, BookUpdateSchema
from src.services import BaseService


class BookService(BaseService):
    model = Book



class BookOtherService:
    async def get_all_books_other(self, session: AsyncSession):
        statement = select(Book)
        result = await session.scalars(statement)
        return result.all()


    async def get_book(self, book_id: int, session: AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await session.scalars(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(
        self, book_data: BookCreateSchema, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        # new_book.published_date = datetime.strptime(
        #     book_data_dict["published_date"], "%Y-%m-%d"
        # )
        session.add(new_book)

        await session.commit()

        return new_book

    async def update_book(
        self, book_id: int, update_data: BookUpdateSchema, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_id, session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()

            return book_to_update
        else:
            return None


    async def delete_book(self, book_id: int, session: AsyncSession):
        book_to_delete = await self.get_book(book_id, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None