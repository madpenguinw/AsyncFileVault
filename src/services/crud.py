from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from db.db import Base
from models.users import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUD(metaclass=ABCMeta):

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError


class FileCRUD(
    CRUD, Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):

    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(
        self, db: AsyncSession, id: int, path: str
    ):
        """Get the file using its id or path"""

        if id:

            statement = (
                select(self._model).
                where(self._model.id == id).
                where(self._model.is_downloadable)
            )

        else:

            statement = (
                select(self._model).
                where(self._model.path == path).
                where(self._model.is_downloadable)
            )

        results = await db.execute(statement=statement)

        return results.scalar_one_or_none()

    async def get_multi(
        self, user: User, db: AsyncSession, skip=0, limit=100
    ):
        """Get all (or as many as it nedeed) downloadable File objects."""

        statement = (
            select(self._model).
            where(self._model.user_id == user.id).
            where(self._model.is_downloadable).
            offset(skip).
            limit(limit)
        )

        results = await db.execute(statement=statement)

        return results.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        filename: str,
        path: str,
        user_id: UUID,
        size: float
    ) -> ModelType:
        """Create the File object in DB."""

        db_obj: Type[ModelType] = self._model(
            name=filename,
            user_id=user_id,
            created_at=datetime.now(),
            path=path,
            size=size,
            is_downloadable=True
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db: AsyncSession,
        id: int,
        path: str,
        user_id: UUID,
    ) -> ModelType:
        """Update the File object."""

        if id:

            statement = (
                update(self._model).
                where(self._model.id == id).
                where(self._model.user_id == user_id).
                where(self._model.is_downloadable == True).  # noqa
                values({'is_downloadable': False}).
                returning(self._model)
            )

        else:

            statement = (
                update(self._model).
                where(self._model.path == path).
                where(self._model.user_id == user_id).
                where(self._model.is_downloadable == True).  # noqa
                values({'is_downloadable': False}).
                returning(self._model)
            )

        results = await db.execute(statement=statement)
        file_obj = results.one_or_none()

        await db.commit()

        return file_obj
