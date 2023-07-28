from typing import Sequence

from app.backend.database import asynch_session, Base
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction, AsyncConnection
from sqlalchemy import select, insert, delete, and_, or_, Result, Row




class BaseDAO:
    current_model: Base | None = None
    session_: AsyncSession = asynch_session()

    @classmethod
    async def add(cls, **model_data):
        async with cls.session_ as session:
            add_query = insert(cls.current_model).values(**model_data).returning(cls.current_model.id)
            post_query_res: id = await session.execute(add_query)
            await session.commit()
            return post_query_res.scalar()

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> current_model:
        async with cls.session_ as session:
            select_query = select(cls.current_model).filter_by(id=user_id)
            query_result = await session.execute(select_query)
            return query_result.scalar_one_or_none()
