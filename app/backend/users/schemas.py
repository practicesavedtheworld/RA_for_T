from pydantic import BaseModel


class UsersScheme(BaseModel):
    username: str
    non_hashed_password: str