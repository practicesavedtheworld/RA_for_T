from sqlalchemy import select

from app.backend.dao.dao import BaseDAO
from app.backend.users.models import Users


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



