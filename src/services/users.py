import logging
import uuid
from typing import Optional

import coloredlogs
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from core.config import app_settings
from models.users import User, get_user_db

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = app_settings.reset_password
    verification_token_secret = app_settings.verification

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        logger.info(
            f'User {user.id} has registered.'
        )

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(
            f'User {user.id} has forgot their password. Reset token: {token}'
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(
            f'Verification requested for user {user.id}. '
            f'Verification token: {token}'
        )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
