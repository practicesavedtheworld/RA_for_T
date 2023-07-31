import pytest

from sqlalchemy.ext.asyncio import AsyncConnection

from app.backend.configurations import settings
from app.backend.targets.models import Targets
from app.backend.users.models import Users
from app.backend.database import asynch_session, Base, engine


@pytest.fixture(scope='function')
async def test_database_preparation():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        connection: AsyncConnection
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
