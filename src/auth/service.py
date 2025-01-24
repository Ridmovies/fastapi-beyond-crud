from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.models import User
from src.auth.schemas import UserCreateSchema
from src.auth.utils import generate_passwd_hash


class UserService:
    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession):
        user_data_dict: dict = user_data.model_dump()
        user = User(**user_data_dict)
        user.password_hash = generate_passwd_hash(user_data_dict.get("password"))
        user.role = "user"
        session.add(user)
        await session.commit()
        return user

    async def get_user_by_email(self, email: str, session: AsyncSession):
        stmt = select(User).where(User.email == email)
        result = await session.scalars(stmt)
        user = result.first()
        return user

    async def get_all_users(self, session: AsyncSession):
        stmt = select(User)
        result = await session.scalars(stmt)
        user = result.all()
        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user else False
