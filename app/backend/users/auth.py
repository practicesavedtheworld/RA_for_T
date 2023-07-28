import logging
from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.backend.configurations import settings
from app.backend.exceptions.token_exceptions import TokenGenerateAttemptFailed

from app.backend.users.dao import UsersDAO
from app.backend.users.exceptions import WrongUsernameOrPassword
from app.backend.users.models import Users

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_hashed_password(user_pass: str) -> str:
    """Transform given str password into stringify hash"""
    hashed_pass = pass_context.hash(user_pass)
    return hashed_pass


def verify_password(for_checking: str, hashed_pass: str) -> bool:
    # TODO handle this with logging
    return pass_context.verify(for_checking, hashed_pass)


def generate_token(data: dict):
    """Generate JWT token """
    to_encode = data.copy()
    expire_on = datetime.utcnow() + timedelta(minutes=60)  # Optional
    to_encode.update({"expiration": str(expire_on)})
    try:
        encoded_jwt_token = jwt.encode(
            to_encode,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        logging.info("Token created successfully")
    except JWTError:
        # log that sh
        raise TokenGenerateAttemptFailed
    return encoded_jwt_token


async def authenticate_user(username: str, password: str) -> bool | None:
    """Checks if the current user exists, and if he does, checks the password field.
    Takes the found existing user before from the database and compares his hashed password with the  given in the function
    """
    user: Users | None = await UsersDAO.get_by_name(username)
    if not user or not verify_password(
            for_checking=password,
            hashed_pass=user.hashed_password
    ):
        # TODO add custom exception
        raise WrongUsernameOrPassword
    return True
