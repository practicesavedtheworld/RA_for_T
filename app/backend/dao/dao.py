from typing import TypeAlias

import fastapi.exceptions
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database import Base, asynch_session
from app.backend.targets.exceptions import TaskAlreadyRemoved
from app.backend.targets.schemas import DeletedTarget, RawTarget
from app.backend.users.exceptions import NoUserFound

SUCCESS_OR_FAILED: TypeAlias = str


class BaseDAO:
    current_model: Base | None = None
    session_: AsyncSession = asynch_session()

    @classmethod
    async def add(cls, **model_data) -> SUCCESS_OR_FAILED:
        async with cls.session_ as session:
            add_query = (
                insert(cls.current_model)
                .values(**model_data)
                .returning(cls.current_model.id)
            )
            post_query_res: id = await session.execute(add_query)
            await session.commit()
            return (
                "Success! Now you can login" if post_query_res else "Failed! Try again"
            )

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> current_model:
        async with cls.session_ as session:
            select_query = select(cls.current_model).filter_by(id=user_id)
            query_result = await session.execute(select_query)
            return query_result.scalar_one_or_none()

    @classmethod
    async def find_all_raw_task(cls, target: RawTarget):
        async with cls.session_ as session:
            select_query = select(cls.current_model.id).filter_by(**target.model_dump())
            query_result = await session.execute(select_query)
            return query_result.scalar()

    @classmethod
    async def delete_task_by_task_id(
        cls, task_id: int, user_id: int | None = None
    ) -> DeletedTarget:
        if not user_id:
            raise NoUserFound

        try:
            async with cls.session_ as session:
                delete_query = (
                    delete(cls.current_model)
                    .filter_by(id=task_id, user_id=user_id)
                    .returning(cls.current_model)
                )
                delete_query_result = await session.execute(delete_query)
                await session.commit()
                return delete_query_result.scalar()
        except fastapi.exceptions.ResponseValidationError:
            raise TaskAlreadyRemoved
