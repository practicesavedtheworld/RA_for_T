from faker import Faker

from app.backend.users.schemas import UsersScheme

fake = Faker()


def get_fake_user():
    fake_user_as_dict = {
        "username": fake.user_name(),
        "non_hashed_password": fake.password(),
    }

    return UsersScheme(**fake_user_as_dict)
