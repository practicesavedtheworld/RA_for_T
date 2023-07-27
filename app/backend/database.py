from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from app.backend.configurations import settings


class Base(DeclarativeBase):
    pass


engine: AsyncEngine = create_async_engine(settings.DB_URL)
asynch_session = async_sessionmaker(bind=engine, expire_on_commit=False)
