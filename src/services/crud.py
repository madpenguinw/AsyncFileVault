from datetime import datetime
from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from db.db import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUD:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class FileCRUD(
    CRUD, Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):

    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(
            self, db: AsyncSession, id: int) -> ModelType | None:
        """Get the file."""
        statement = select(self._model).where(
            self._model.id == id and self._model.is_downloadable)
        results = await db.execute(statement=statement)

        return results.scalar_one_or_none()

    async def get_multi(
        self, user_id: int, db: AsyncSession, skip=0, limit=100
    ) -> list[ModelType]:
        """Get all downloadable(or as many as it nedeed) File objects."""

        statement = select(self._model).where(
            self._model.user == user_id).where(
                self._model.is_downloadable).offset(skip).limit(limit)
        results = await db.execute(statement=statement)

        return results.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType
    ) -> ModelType:
        """Create the File object in DB."""

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """Update the File object."""

        obj_in_data = jsonable_encoder(obj_in)
        safe_dict: dict[str, Any] = {}
        for item in obj_in_data.items():
            if item[1] is not None:  # value can be False, but not None
                safe_dict[item[0]] = item[1]
        statement = update(self._model).where(
            self._model.id == db_obj.id).values(
                safe_dict).returning(self._model)

        results = await db.execute(statement=statement)
        file_obj = results.one_or_none()

        await db.commit()

        return file_obj
