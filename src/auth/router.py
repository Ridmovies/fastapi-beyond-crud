from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from src.auth.schemas import UserCreateSchema, UserSchema, UserLoginSchema
from src.auth.service import UserService
from src.auth.utils import verify_password, create_access_token
from src.database import SessionDep

router = APIRouter()
user_service = UserService()


REFRESH_TOKEN_EXPIRY = 2

@router.get("", response_model=list[UserSchema])
async def get_all_users(session: SessionDep):
    return await user_service.get_all_users(session)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user_account(user_data: UserCreateSchema, session: SessionDep):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="email already exists"
        )

    return await user_service.create_user(user_data, session)



@router.post("/login")
async def login_user(login_data: UserLoginSchema, session: SessionDep):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session)
    if user:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),

                }
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid email or password"
        )





