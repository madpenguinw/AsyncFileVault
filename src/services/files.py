from fastapi import UploadFile

from models.files import File as FileModel
from schemas.files import File
from services.crud import FileCRUD


class RepositoryFile(FileCRUD[FileModel, UploadFile, File]):
    pass


file_crud = RepositoryFile(FileModel)
