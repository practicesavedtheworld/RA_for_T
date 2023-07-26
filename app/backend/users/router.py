from fastapi import APIRouter, HTTPException, status
from starlette.responses import Response

from app.backend.users.auth import create_hashed_password, authenticate_user
from app.backend.users.dao import UsersDAO
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
        )


@router.post('/login')
async def login(abc_user: UsersScheme, response: Response):
    """Add token for user if user pass the authentication & authorisation"""

    user_exist = await UsersDAO.get_by_name(abc_user.username)
    if not user_exist:
        # TODO add custom exp
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
        )
    user_passed_validation = await authenticate_user(user_exist.username, abc_user.non_hashed_password)
    return "EST", user_passed_validation
