from fastapi import Request, HTTPException, Depends

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.utils import decode_token


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        # if await token_in_blocklist(token_data["jti"]):
        #     raise InvalidToken()

        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )


# async def get_current_user(
#     token_details: dict = Depends(AccessTokenBearer()),
#     session: AsyncSession = Depends(get_session),
# ):
#     user_email = token_details["user"]["email"]
#     user = await user_service.get_user_by_email(user_email, session)
#     return user
