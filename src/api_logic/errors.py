from fastapi import HTTPException, status


def file_not_found_error():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='File was not found.'
    )


def file_not_saved_error():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='File was not saved.'
    )


def file_gone_error():
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail='File was deleted from the database.'
    )


def internal_server_error():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Internal Server Error'
    )
