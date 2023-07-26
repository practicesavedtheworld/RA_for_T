from fastapi import APIRouter


router = APIRouter(
    prefix='/users',
    tags=['Auth & Users'],
)

