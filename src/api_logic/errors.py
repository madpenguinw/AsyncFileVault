from fastapi import HTTPException, status


def file_not_found_error(detail: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )


def bad_request_error(detail: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def permission_denied_error(detail: str):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )
