from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_by_id(cls, model_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_by_uid(cls, model_uid: str):
        async with async_session() as session:
            query = select(cls.model).filter_by(uid=model_uid)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, data, user_uid: str):
        async with async_session() as session:
            data_dict = data.model_dump()
            instance = cls.model(**data_dict)
            instance.user_uid = user_uid
            session.add(instance)
            await session.commit()
            return instance

    @classmethod
    async def delete(cls, model_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                await session.delete(instance)
                await session.commit()

    @classmethod
    async def update(cls, model_id: int, update_data):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                for key, value in update_data.model_dump().items():
                    setattr(instance, key, value)
                await session.commit()
                return instance
            else:
                raise Exception("No such instance")

    @classmethod
    async def patch(cls, model_id: int, update_data):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(instance, key, value)
                await session.commit()
                return instance
            else:
                raise Exception("No such instance")
