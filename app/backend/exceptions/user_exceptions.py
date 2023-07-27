from fastapi import HTTPException


class BaseUserException(HTTPException):
    details = ''
    exception_status_code = 500

    def __init__(self):
        super().__init__(detail=self.details, status_code=self.exception_status_code)

    def __str__(self):
        return super().__repr__()
