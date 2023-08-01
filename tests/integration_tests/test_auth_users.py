import pytest
from sqlalchemy import select

from app.backend.users.models import Users


class TestUserAuthentication:

    @pytest.mark.parametrize("status", [
        200,
        409,
    ])
    async def test_new_user_registration(self, status, test_database_preparation, ac, fake_user):
        """Test user registration two times"""

        registration = await ac.post(url='/users/register', json=fake_user.model_dump())
        assert registration.status_code == status

    async def test_login(self, ac, db_session, fake_user):
        login = await ac.post(url="/users/login", json=fake_user.model_dump())
        assert login.status_code == 200

        get_user_id_query = select(Users.id).select_from(Users)
        get_user_id_query_result = await db_session.execute(get_user_id_query)
        assert get_user_id_query_result.scalar() == 1

    async def test_myself(self, ac, fake_user):
        me = await ac.post(url="/users/login", json=fake_user.model_dump())
        assert me.status_code == 200
