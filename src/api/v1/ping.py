import asyncio
import logging

import coloredlogs
from async_timeout import timeout
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from db.db import get_session
from models.files import File as FileModel
from models.users import User as UserModel

ping_router = APIRouter(tags=['Check ping'])

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


@ping_router.get(
    '/',
    status_code=status.HTTP_200_OK
)
async def ping_database(
    db: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    """
    Check if the database is available.
    """

    try:
        async with timeout(1):
            await asyncio.gather(
                db.execute(select(UserModel)),
                db.execute(select(FileModel))
            )
    except TimeoutError:
        logger.critical('Database is unavailable')
        raise HTTPException(
            {'db': 'Unavailable'},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    return {'db': 'Available'}
