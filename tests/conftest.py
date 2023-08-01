import asyncio
from httpx import AsyncClient

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection

from app.backend.configurations import settings
from app.backend.targets.models import Targets
from app.backend.users.models import Users
from app.backend.database import asynch_session, Base, engine
from main import app as fastapi_app
from tests.utils import get_fake_user

async_client = AsyncClient(app=fastapi_app, base_url='http://testing/')


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


@pytest.fixture(scope='session')
async def ac():
    async with async_client as a_c:
        yield a_c


@pytest.fixture(scope='function')
async def db_session():
    async with asynch_session() as session:
        yield session


@pytest.fixture(scope='session')
def fake_user():
    return get_fake_user()


@pytest.fixture(scope='class')
async def authenticated_user_session():
    fake_user = get_fake_user()
    # new AsyncClient instance
    async with AsyncClient(app=fastapi_app, base_url='http://testing/') as session:
        registration = await session.post(url="/users/register", json=fake_user.model_dump())
        login = await session.post(url="/users/login", json=fake_user.model_dump())
        assert login.status_code == 200 and registration.status_code == 200
        yield session
