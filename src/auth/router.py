from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer
from src.auth.schemas import UserCreateSchema, UserSchema, UserLoginSchema
from src.auth.service import UserService
from src.auth.utils import verify_password, create_access_token
from src.database import SessionDep

router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()
REFRESH_TOKEN_EXPIRY = 2

# Bearer Token

# curl -X 'GET' \
#   'http://127.0.0.1:8000/api/v1/auth' \
#   -H 'accept: application/json' \
#   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoic3RyaW5nIiwidXNlcl91aWQiOiJiYzJkODZlZi0yODE3LTRlYmEtOTI3Zi0zNzY2ZjVjMGYxNjAifSwiZXhwIjoxNzM2OTY2MTQ5LCJqdGkiOiIyMDFjYmI4MC1iMjQ5LTRiZDMtYTFiZS02MzgyZDZkMjQyOWUiLCJyZWZyZXNoIjpmYWxzZX0.hnxuYsF5a8wzvSS5oO63uLAkFxQ6ikatXR3RUgEmEGw'

@router.get("", response_model=list[UserSchema])
async def get_all_users(session: SessionDep, user_details=Depends(access_token_bearer)):
    print(f"{user_details=}")
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


@router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid refresh token")


