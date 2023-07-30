from fastapi import HTTPException, status


class BaseTargetException(HTTPException):
    detail = 'Internal server error'
    exception_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self):
        super().__init__(status_code=self.exception_status_code, detail=self.detail)

