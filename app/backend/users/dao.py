from app.backend.dao.dao import BaseDAO
from app.backend.users.models import Users

from sqlalchemy import select, column, text


class UsersDAO(BaseDAO):
    current_model = Users

    @classmethod
    async def get_by_name(cls, name) -> Users:
        async with cls.session_ as session:
            user = select(cls.current_model).where(
                cls.current_model.__table__.c.username == name
            )
            query_res = await session.execute(user)
            user_model: Users = query_res.scalar_one_or_none()
            return user_model

    @classmethod
    async def get_by_id(cls, id_: int) -> current_model:
        async with cls.session_ as session:
            select_query = select(cls.current_model).filter_by(id=id_)
            query_result = await session.execute(select_query)
            return query_result.scalar_one_or_none()

