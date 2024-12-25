from fastapi import APIRouter, HTTPException, status

from src.auth.models import User
from src.auth.schemas import UserCreateSchema
from src.auth.service import UserService
from src.database import SessionDep

router = APIRouter()
user_service = UserService()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateSchema, session: SessionDep):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="email already exists"
        )

    return await user_service.create_user(user_data, session)



@router.get("")
async def get_all_users(session: SessionDep):
    return await user_service.get_all_users(session)