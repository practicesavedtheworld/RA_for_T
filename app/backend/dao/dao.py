from app.backend.database import asynch_session, Base
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction, AsyncConnection
from sqlalchemy import select, insert, delete, and_, or_

from app.backend.targets.models import Targets


class BaseDAO:
    current_model: Base | None = None
    session_: AsyncSession = asynch_session()

    @classmethod
    async def add(cls, **model_data):
        async with cls.session_ as session:
            add_query = insert(cls.current_model).values(**model_data)
            post_query_res = await session.execute(add_query)
            print(post_query_res.scalar())
            await session.commit()

    @classmethod
    async def get_by_id(cls, id: int):
        async with cls.session_ as session:
            select_query = select(cls.current_model).filter_by(user_id=id)
            r = await session.execute(select_query)
            print(r.all())






