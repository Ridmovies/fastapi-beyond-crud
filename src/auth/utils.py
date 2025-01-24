import logging
import uuid
from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from passlib.context import CryptContext

from src.config import settings

passwd_context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRY = 3600


def generate_passwd_hash(password: str) -> str:
    hash_password = passwd_context.hash(password)
    return hash_password


def verify_password(password: str, hash_password: str) -> bool:
    return passwd_context.verify(password, hash_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    token = jwt.encode(
        payload=payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return token


def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

