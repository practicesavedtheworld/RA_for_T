import jose
from passlib.context import CryptContext
from starlette.exceptions import HTTPException
from starlette import status

from app.backend.users.dao import UsersDAO
from app.backend.users.models import Users

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_hashed_password(user_pass: str) -> str:
    hashed_pass = pass_context.hash(user_pass)
    return hashed_pass


def verify_password(for_checking: str, hashed_pass: str) -> bool:
    return pass_context.verify(for_checking, hashed_pass)


async def authenticate_user(username: str, password: str) -> bool | None:
    user: Users | None = await UsersDAO.get_by_name(username)
    if not user or not verify_password(
            for_checking=password,
            hashed_pass=user.hashed_password
    ):
        # TODO add custom exception
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
