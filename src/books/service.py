from src.books.models import Book
from src.services import BaseService


class BookService(BaseService):
    model = Book
