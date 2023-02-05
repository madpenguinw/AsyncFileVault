from datetime import datetime

from pydantic import BaseModel


class Settings(BaseModel):
    class Config:
        orm_mode = True


class FileBase(BaseModel):
    """Shared File properties"""
    path: str


class File(FileBase, Settings):
    """Full File properties in DB"""
    id: int
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool
