from fastapi import status

from app.backend.exceptions.user_exceptions import BaseUserException


class TokenClosedOrNeverExisted(BaseUserException):
    details = "Token does not exist"
    exception_status_code = status.HTTP_401_UNAUTHORIZED


class TokenTimeoutOrWrongSecrets(BaseUserException):
    details = ''
    exception_status_code = status.HTTP_401_UNAUTHORIZED


class NoUserFound(BaseUserException):
    details = 'No any user found with that id'
    exception_status_code = status.HTTP_404_NOT_FOUND


class WrongUsernameOrPassword(BaseUserException):
    details = 'Wrong login or password'
    exception_status_code = status.HTTP_401_UNAUTHORIZED


class UsernameAlreadyTaken(BaseUserException):
    details = 'Username already taken by another user. Choose another'
    exception_status_code = status.HTTP_409_CONFLICT
