from fastapi import Depends
from fastapi_users_db_sqlalchemy import (SQLAlchemyBaseUserTableUUID,
                                         SQLAlchemyUserDatabase)
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase, SQLAlchemyBaseAccessTokenTableUUID)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from db.db import Base, get_session


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'user'
    files = relationship(
        'File', back_populates='user', passive_deletes=True
    )


async def get_access_token_db(
    session: AsyncSession = Depends(get_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
