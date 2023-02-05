import os

from core.config import app_settings


def get_file_sizes(paths: list[str]) -> int | float:
    """Returns sum of file sizes in bytes"""
    size: int | float = 0

    for path in paths:
        size += os.path.getsize(path)

    return size


def get_filename_path(username: str, filename: str, path: str) -> list[str]:
    """Returns a list with the name of the file and the path to it"""
    head, tail = os.path.split(path)

    if '.' in tail:
        filename = tail
        path = path.split('/' + filename, maxsplit=1)[0]

    path = f'{app_settings.file_path}/{username}/{path}/'
    path = os.path.normpath(path)

    return [filename, path]
