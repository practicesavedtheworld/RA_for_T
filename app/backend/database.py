from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.backend.configurations import settings

if settings.MODE == "TEST":
    DB_URL = settings.TEST_DB_URL
else:
    DB_URL = settings.DB_URL


class Base(DeclarativeBase):
    pass


engine: AsyncEngine = create_async_engine(DB_URL)
asynch_session = async_sessionmaker(bind=engine, expire_on_commit=False)
