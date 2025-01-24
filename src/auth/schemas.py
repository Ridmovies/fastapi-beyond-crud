import uuid
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from src.books.models import Book


class UserCreateSchema(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=4)
    first_name: str
    last_name: str
    # role: str = Field(default="user")


class UserSchema(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime
    role: str


class UserLoginSchema(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=4)


class UserBookSchema(UserSchema):
    books: list["Book"]