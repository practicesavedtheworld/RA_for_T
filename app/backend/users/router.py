from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import Response

from app.backend.exceptions.user_exceptions import WrongUsernameOrPassword, UsernameAlreadyTaken
from app.backend.users.auth import create_hashed_password, authenticate_user, generate_token
from app.backend.users.dao import UsersDAO
from app.backend.users.dependencies import get_current_user
from app.backend.users.models import Users
from app.backend.users.schemas import UsersScheme

router = APIRouter(
    prefix='/users',
    tags=['Auth & Users'],
)


@router.post('/register')
async def new_user_registration(user: UsersScheme):
    """Creates new user if user with this username does not exist.
    Store in db hashed password"""

    user_exist = await UsersDAO.get_by_name(user.username)
    if not user_exist:
        hashed_pass = create_hashed_password(user.non_hashed_password)
        await UsersDAO.add(username=user.username, hashed_password=hashed_pass)
    else:
        raise UsernameAlreadyTaken


@router.post('/login')
async def login(abc_user: UsersScheme, response: Response):
    """Add token for user if user pass the authentication & authorisation"""

    user_exist = await UsersDAO.get_by_name(abc_user.username)
    if not user_exist:
        # TODO add custom exp
        raise WrongUsernameOrPassword

    user_that_passed_validation: bool = await authenticate_user(user_exist.username, abc_user.non_hashed_password)
    if user_that_passed_validation:
        user_token = generate_token({"sub": str(user_exist.id)})
        response.set_cookie(
            'targets_user_token',
            user_token,
            httponly=True,
        )
    return user_that_passed_validation


@router.post('/me')
async def myself(user: Users = Depends(get_current_user)):
    return user
