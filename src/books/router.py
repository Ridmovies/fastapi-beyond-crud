from fastapi import APIRouter

from src.books.schemas import (
    BookCreateSchema,
    BookSchema,
    BookUpdateSchema,
    BookPatchSchema,
)
from src.books.service import BookService, BookOtherService
from src.database import SessionDep

router = APIRouter()

book_service = BookOtherService()


### First option for using the BookService without session


@router.get("/", response_model=list[BookSchema])
async def get_all_books():
    books = await BookService.get_all()
    return books


@router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int):
    book = await BookService.get_one_by_id(model_id=book_id)
    return book


@router.post("/", response_model=BookSchema)
async def create_book(book_data: BookCreateSchema):
    book = await BookService.create(data=book_data)
    return book


@router.delete("/{book_id}")
async def delete_book(book_id: int):
    await BookService.delete(model_id=book_id)


@router.put("/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, update_data: BookUpdateSchema):
    book = await BookService.update(model_id=book_id, update_data=update_data)
    return book


@router.patch("/{book_id}", response_model=BookSchema)
async def patch_book(book_id: int, update_data: BookPatchSchema):
    book = await BookService.patch(model_id=book_id, update_data=update_data)
    return book


### Second option for using the BookService with session
@router.get("/other/all", response_model=list[BookSchema])
async def get_all_books(session: SessionDep):
    books = await book_service.get_all_books_other(session=session)
    return books


@router.get("/other/{book_id}", response_model=BookSchema)
async def get_book(book_id: int, session: SessionDep):
    book = await book_service.get_book(book_id, session)
    return book


@router.post("/other", response_model=BookSchema)
async def create_book(book_data: BookCreateSchema, session: SessionDep):
    book = await book_service.create_book(book_data, session)
    return book


@router.put("/other/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, update_data: BookUpdateSchema, session: SessionDep):
    book = await book_service.update_book(book_id, update_data, session)
    return book


@router.delete("/other/{book_id}")
async def delete_book(book_id: int, session: SessionDep):
    await book_service.delete_book(book_id, session)
