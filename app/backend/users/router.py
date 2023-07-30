from typing import TypeAlias

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.backend.users.auth import (
    authenticate_user,
    create_hashed_password,
    generate_token,
)
from app.backend.users.dao import UsersDAO
from app.backend.users.dependencies import get_current_user
from app.backend.users.exceptions import UsernameAlreadyTaken, WrongUsernameOrPassword
from app.backend.users.models import Users
from app.backend.users.schemas import UsersScheme

router = APIRouter(
    prefix="/users",
    tags=["Auth & Users"],
)
USER_ID: TypeAlias = int


@router.post("/register")
async def new_user_registration(user: UsersScheme) -> str:
    """Creates new user if user with this username does not exist.
    Store in db hashed password"""

    user_exist = await UsersDAO.get_by_name(user.username)
    if user_exist:
        raise UsernameAlreadyTaken
    hashed_pass = create_hashed_password(user.non_hashed_password)
    return await UsersDAO.add(username=user.username, hashed_password=hashed_pass)


@router.post("/login")
async def login(abc_user: UsersScheme, response: Response) -> USER_ID:
    """Add token for user if user pass the authentication & authorisation"""

    user_exist = await UsersDAO.get_by_name(abc_user.username)
    if not user_exist:
        raise WrongUsernameOrPassword

    user_that_passed_validation: bool = await authenticate_user(
        user_exist.username, abc_user.non_hashed_password
    )
    if user_that_passed_validation:
        user_token = generate_token({"sub": str(user_exist.id)})
        response.set_cookie(
            "targets_user_token",
            user_token,
            httponly=True,
        )
    return user_exist.id


@router.post("/me")
async def myself(user: Users = Depends(get_current_user)) -> dict:
    """Return to client user info without hashed password"""

    return {"id": user.id, "username": user.username}
