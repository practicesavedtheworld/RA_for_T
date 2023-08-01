from faker import Faker

from app.backend.targets.schemas import RawTarget
from app.backend.users.schemas import UsersScheme

fake = Faker()


def get_fake_user() -> UsersScheme:
    fake_user_as_dict = {
        "username": fake.user_name(),
        "non_hashed_password": fake.password(),
    }

    return UsersScheme(**fake_user_as_dict)


def get_fake_raw_target(
        title: str = fake.word(),
        description: str = fake.text(max_nb_chars=250),
        status: str = "new",
) -> RawTarget:
    target = {
        "title": title,
        "description": description,
        "status": status,
    }
    return RawTarget(**target)
