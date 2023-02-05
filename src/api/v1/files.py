import logging
import os
import shutil
from pathlib import Path
from typing import Any

import aiofiles
import coloredlogs
from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     Response, UploadFile, status)
from sqlalchemy.ext.asyncio import AsyncSession

from api_logic.errors import (file_gone_error, file_not_found_error,
                              file_not_saved_error, internal_server_error)
from api_logic.logic import get_file_sizes, get_filename_path
from db.db import get_session
from models.files import File as FileModel
from models.users import User
from schemas.files import File as FileSchema
from schemas.files import FileBase as FileBaseSchema
from services.authentication import current_user
from services.files import file_crud

files_router = APIRouter(tags=['Manage files'])

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


@files_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=dict[str, list[FileSchema]]
)
async def get_files_info(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    max_result: int = 10,
    offset: int = 0
) -> dict[str, list[FileSchema]]:
    """
    Get File objects.
    """

    user_id = user.id

    files = await file_crud.get_multi(
        db=db, user_id=user_id, limit=max_result, skip=offset
    )

    if not files:
        logger.error(
            'Files, uploaded by user with ID="%(user_id)s", '
            'were not found in database',
            {'user_id': user_id}
        )
        file_not_found_error()

    return {'account_id': user.id, 'files': [files]}


@files_router.post(
    '/upload',
    response_model=FileSchema,
    status_code=status.HTTP_201_CREATED
)
async def upload_file(
    *,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
    file_obj: FileBaseSchema,
    file: UploadFile = File(),
    response: Response
) -> FileSchema:
    """
    Upload file to DB.
    """

    path = file_obj.path

    filename: str = file.filename
    username: str = str(user.id)
    res_filename_path_list: list[str] = get_filename_path(
        username, filename, path
    )
    real_filename: str = res_filename_path_list[0]
    real_path: str = res_filename_path_list[1]

    if not Path.exists(real_path):
        Path(real_path).mkdir(parents=True, exist_ok=True)
        logger.info('Path "%(path)s" was created', {'path': path})

    try:
        file.file.seek(0)
        content = file.file.read()

        async with aiofiles.open(
            Path(path, real_filename), 'wb'
        ) as server_file:
            await server_file.write(content)

    except Exception as error:
        logger.error(error)
        file_not_saved_error()

    file = await file_crud.create(
        db=db, file=file, user=user, path=path
    )

    logger.debug(
        'File "%(file)s" was successfully uploaded to server and saved in DB',
        {'file': real_filename}
    )

    return file
