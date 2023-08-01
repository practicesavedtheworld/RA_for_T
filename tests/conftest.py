import asyncio
from httpx import AsyncClient

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection

from app.backend.configurations import settings
from app.backend.targets.models import Targets
from app.backend.users.models import Users
from app.backend.database import asynch_session, Base, engine
from app.backend.users.schemas import UsersScheme
from main import app as fastapi_app


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='class')
async def test_database_preparation():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        connection: AsyncConnection
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def test_database_clear():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://testing/') as a_c:
        yield a_c


@pytest.fixture()
async def db_session():
    async with asynch_session() as session:
        yield session


@pytest.fixture()
def fake_user():
    fake_user_as_dict = {
        "username": "1qa",
        "non_hashed_password": "11"
    }
    return UsersScheme(**fake_user_as_dict)
