import uuid

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)

from core.config import app_settings
from models.users import User
from services.users import get_user_manager


class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> str | None:
        from fastapi import status
        try:
            r = await super().__call__(request)
            token = r.credentials
        except HTTPException as ex:
            assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
            token = None
        return token


auth_scheme = OptionalHTTPBearer()

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=app_settings.verification,
        lifetime_seconds=36000
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
