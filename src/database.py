from typing import Annotated

from fastapi import Depends
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
DATABASE_PARAMS = {"poolclass": NullPool}


# async_engine = create_async_engine(url=DATABASE_URL, echo=True)
async_engine = AsyncEngine(create_engine(url=DATABASE_URL, echo=True, **DATABASE_PARAMS))
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

# class Base(DeclarativeBase): ...


async def get_session():
    async with async_session() as session:
        yield session

# AsyncSession from sqlmodel.ext.asyncio.session
SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def init_models() -> None:
    """Create tables if they don't already exist.

    In a real-life example we would use Alembic to manage migrations.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)  # noqa: ERA001
        await conn.run_sync(SQLModel.metadata.create_all)

