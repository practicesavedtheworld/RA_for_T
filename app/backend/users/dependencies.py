import logging
from datetime import datetime as dt
from typing import TypeAlias

from fastapi import Depends
from jose import jwt, JWTError
from starlette.requests import Request

from app.backend.app_logging import create_logger
from app.backend.configurations import settings
from app.backend.users.dao import UsersDAO
from app.backend.users.exceptions import (
    TokenClosedOrNeverExisted,
    TokenTimeoutOrWrongSecrets,
    NoUserFound,
    ConnectionErrorOrBadRequest,
)
from app.backend.users.models import Users

Token: TypeAlias = str
dependencies_logger = create_logger(
    level=logging.ERROR,
    file_name='critical&error.log',
    loger_name='dependencies_logger'
)


def get_user_token(request: Request) -> Token:
    """Get user token from cookies"""

    try:
        token = request.cookies.get("targets_user_token")
        if not token:
            raise TokenClosedOrNeverExisted
        return token
    except (AttributeError, NameError):
        dependencies_logger.error(f"[{get_user_token.__name__}]\t Could not get token from request")
        raise ConnectionErrorOrBadRequest


async def get_current_user(token: Token = Depends(get_user_token)) -> Users:
    """Decoding token and checking if it's available.
    Checks:
           1) Token expiration
           2) Token existence (if secret key or algo are wrongs - token does not exist)
           3) Token bounding with user"""

    try:
        decoded_jwt_token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_expiration: str = decoded_jwt_token.get("expiration")
    except JWTError:
        dependencies_logger.error(
            f"[{get_current_user.__name__}]\t Someone tried to login with an old token or re-login required",
        )
        raise TokenClosedOrNeverExisted

    time_at_this_moment: float = dt.utcnow().timestamp()
    if not decoded_jwt_token or dt.strptime(token_expiration, "%Y-%m-%d %H:%M:%S.%f").timestamp() < time_at_this_moment:
        raise TokenTimeoutOrWrongSecrets

    user_id: str = decoded_jwt_token.get("sub")
    user: Users = await UsersDAO.get_by_user_id(int(user_id))
    if not user_id or not user:
        dependencies_logger.error(f" User not found or deleted while token is still alive")
        raise NoUserFound
    return user
