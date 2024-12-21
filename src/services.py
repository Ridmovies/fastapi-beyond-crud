from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import a_session


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, **filter_by):
        async with a_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with a_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_by_id(cls, model_id: int):
        async with a_session() as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **data):
        async with a_session() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.commit()
            return instance
