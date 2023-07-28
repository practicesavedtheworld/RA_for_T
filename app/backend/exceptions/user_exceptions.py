from fastapi import HTTPException, status


class BaseUserException(HTTPException):
    details = ''
    exception_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self):
        super().__init__(detail=self.details, status_code=self.exception_status_code)

    def __str__(self):
        return super().__repr__()
