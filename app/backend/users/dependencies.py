from datetime import datetime

from fastapi import Depends
from jose import jwt, JWTError
from starlette.requests import Request

from app.backend.configurations import settings
from app.backend.users.dao import UsersDAO
from app.backend.users.models import Users


def get_user_token(request: Request) -> str:
    try:
        token = request.cookies.get("targets_user_token")
        if not token:
            # raise timeout token
            ...
        return token
    except:
        # log that
        ...


async def get_current_user(token: str = Depends(get_user_token)):
    """ """
    decoded_jwt_token, token_expiration = dict, ''
    try:
        decoded_jwt_token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_expiration: str = decoded_jwt_token.get("expiration")
    except JWTError:
        # token does not exist, gone
        ...
    if not decoded_jwt_token or datetime.strptime(token_expiration, "%Y-%m-%d %H:%M:%S.%f").timestamp() > datetime.utcnow().timestamp():
        #  Logg and raise ex
        ...
    user_id: str = decoded_jwt_token.get("sub")
    user: Users = await UsersDAO.get_by_id(int(user_id))
    if not user_id or not user:
        # user doesnt exist + log
        ...
    return user

