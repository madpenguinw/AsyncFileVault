import logging

import coloredlogs
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api_logic.errors import file_not_found_error
from api_logic.logic import get_file_sizes
from db.db import get_session
from models.users import User
from services.authentication import auth_scheme, current_user
from services.files import file_crud

user_router = APIRouter(tags=['User status'])

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


@user_router.get(
    '/status',
    status_code=status.HTTP_200_OK
)
async def get_status(
    *,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
) -> dict:
    """
    Return information about disk space usage status
    and previously downloaded files.
    """

    files = await file_crud.get_multi(
        db=db, user=user, limit=10000, skip=0
    )

    if not files:
        logger.error(
            'Files, uploaded by user with ID="%(user_id)s", '
            'were not found in database',
            {'user_id': user.id}
        )
        file_not_found_error('Files were not found.')

    try:
        size: int | float = get_file_sizes(files=files)
    except FileNotFoundError:
        file_not_found_error('Files were not found.')

    length: int = len(files)

    return {'account_id': user.id, 'files': length, 'used': size}
