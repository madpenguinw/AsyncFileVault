import os

from core.config import app_settings
from models.files import File


def get_file_sizes(path: str = '', files: list[File] = []) -> int | float:
    """Returns sum of file sizes in bytes"""

    size: int | float = 0

    if files:
        for file in files:
            size += os.path.getsize(file.path)
    elif path:
        size += os.path.getsize(path)

    return size


def get_filename_path(username: str, filename: str, path: str) -> list[str]:
    """Returns a list with the name of the file and the path to it"""
    head, tail = os.path.split(path)

    if '.' in tail:
        filename = tail
        path = path.split('/' + filename, maxsplit=1)[0]

    path = f'{app_settings.files_dir}/{username}/{path}/'
    path = os.path.normpath(path)

    return [filename, path]
