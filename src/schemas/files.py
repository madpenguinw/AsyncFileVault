from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Settings(BaseModel):
    class Config:
        orm_mode = True


class FileBase(BaseModel):  # not using this class for now
    """Shared File properties"""
    path: str


class File(FileBase, Settings):
    """Full File properties in DB"""
    id: int
    user_id: UUID  # unrequired additional param
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool
