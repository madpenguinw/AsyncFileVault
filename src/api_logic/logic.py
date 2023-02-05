import os

from core.config import app_settings
from models.files import File


def get_file_sizes(files: list[File]) -> int | float:
    """Returns sum of file sizes in bytes"""
    size: int | float = 0

    for file in files:
        size += os.path.getsize(file.path)

    return size


def get_filename_path(username: str, filename: str, path: str) -> list[str]:
    """Returns a list with the name of the file and the path to it"""
    path = os.path.normpath(path)
    head, tail = os.path.split(path)

    if '.' in tail:
        filename = tail
        path = path.split('/' + filename, maxsplit=1)[0]

    path = f'{app_settings.path}/{username}/{path}/{filename}'

    return [filename, path]
