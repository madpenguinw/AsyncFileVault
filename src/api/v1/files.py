import logging
import os
from pathlib import Path
from uuid import UUID

import aiofiles
import coloredlogs
from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api_logic.errors import (bad_request_error, file_not_found_error,
                              permission_denied_error)
from api_logic.logic import get_file_sizes, get_filename_path
from db.db import get_session
from models.users import User
from schemas.files import File as FileSchema
from services.authentication import auth_scheme, current_user
from services.files import file_crud

files_router = APIRouter(tags=['Manage files'])

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


@files_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=dict[str, list[FileSchema] | UUID]
)
async def get_files_info(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    max_result: int = 10,
    offset: int = 0
) -> dict[str, list[FileSchema] | UUID]:
    """
    Get File objects.
    """

    files = await file_crud.get_multi(
        db=db, user=user, limit=max_result, skip=offset
    )

    if not files:
        logger.error(
            'Files, uploaded by user with ID="%(user_id)s", '
            'were not found in database',
            {'user_id': user.id}
        )
        file_not_found_error('Files were not found.')

    return {'account_id': user.id, 'files': files}


@files_router.post(
    '/upload',
    response_model=FileSchema,
    status_code=status.HTTP_201_CREATED
)
async def upload_file(
    *,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    path: str = '',
    file: UploadFile = File(),
) -> FileSchema:
    """
    Upload file to DB.
    Path here is a relative path,
    where the root directory is a folder with the user name.
    """

    filename: str = file.filename
    username: str = str(user.id)
    res_filename_path_list: list[str] = get_filename_path(
        username=username, filename=filename, path=path
    )
    real_filename: str = res_filename_path_list[0]
    real_path: str = res_filename_path_list[1]

    Path(real_path).mkdir(parents=True, exist_ok=True)
    logger.info('Path "%(path)s" was created', {'path': real_path})

    try:
        file.file.seek(0)
        content = file.file.read()

        async with aiofiles.open(
            Path(real_path, real_filename), 'wb'
        ) as server_file:
            await server_file.write(content)

        logger.info(
            'File "%(filename)s" was saved on server',
            {'filename': filename}
        )

    except Exception as error:
        logger.error(error)
        bad_request_error('File was not saved.')

    real_full_path = f'{real_path}\\{real_filename}'

    size = get_file_sizes([real_full_path])

    file = await file_crud.create(
        db=db,
        filename=real_filename,
        user_id=username,
        path=real_full_path,
        size=size
    )

    logger.debug(
        'File "%(file)s" was successfully uploaded to server and saved in DB',
        {'file': real_filename}
    )

    return file


@files_router.get(
    '/download',
    response_class=FileResponse,
    status_code=status.HTTP_200_OK
)
async def download_file(
    *,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    path: str,  # it also may be an id
) -> FileResponse:
    """
    Download file from DB.
    Path here is an absolute path to file (Use one slash in it).
    Path should include file's name.
    Due to technical task path variable may also be a file's id.
    Only user who upload the file can download it.
    """

    id = 0

    try:
        id = int(path)
    except ValueError:
        pass

    try:
        file = await file_crud.get(
            db=db,
            id=id,
            path=path,
        )
    except Exception as error:
        logger.error(error)
        file_not_found_error('Exception during handling the request.')

    if not file:
        logger.error('File "%(path)s" was not found', {'path': path})
        file_not_found_error('File was not found.')

    if file.user_id != user.id:
        permission_denied_error('Permission denied.')

    logger.debug(
        'File "%(path)s" was successfully downloaded '
        'from server and saved in DB',
        {'path': path}
    )

    return file.path


@files_router.get(
    '/delete',
    status_code=status.HTTP_404_NOT_FOUND
)
async def delete_file(
    *,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    path: str,  # it also may be an id
) -> FileResponse:
    """
    Delete file from DB.
    Path here is an absolute path to file (Use one slash in it).
    Path should include file's name.
    Due to technical task path variable may also be a file's id.
    Only user who upload the file can delete it.
    """

    id = 0

    try:
        id = int(path)
    except ValueError:
        pass

    try:
        file = await file_crud.update(
            db=db,
            id=id,
            path=path,
            user_id=user.id
        )
    except Exception as error:
        logger.error(error)
        file_not_found_error('Exception during handling the request.')

    if not file:
        logger.error('File "%(path)s" was not found', {'path': path})
        file_not_found_error('File was not found.')

    try:
        os.unlink(file.path)
    except Exception as error:
        logger.error(error)
        file_not_found_error('Exception during handling the request.')

    logger.debug(
        'File "%(path)s" was successfully deleted from server',
        {'path': path}
    )

    return file
