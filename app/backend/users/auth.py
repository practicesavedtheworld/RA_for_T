import jose
from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_hashed_password(user_pass: str) -> str:
    hashed_pass = pass_context.hash(user_pass)
    return hashed_pass


def verify_password(for_checking: str, hashed_pass: str) -> bool:
    return pass_context.verify(for_checking, hashed_pass)
