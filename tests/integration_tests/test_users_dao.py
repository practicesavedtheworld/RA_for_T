from app.backend.targets.dao import TargetsDAO

from tests.utils import get_fake_raw_target


class TestAuthenticatedUserTargetsDAOManipulations:
    """Basic CRUD DAO testing"""

    async def test_new_task(self, test_database_preparation, authenticated_user_session):
        resp = await authenticated_user_session.post(
            url='/tasks',
            json=get_fake_raw_target().model_dump(),
        )

        assert resp.status_code == 200

    async def test_update_task(self, authenticated_user_session):
        task_id = await TargetsDAO.find_all_raw_task(get_fake_raw_target())
        resp = await authenticated_user_session.put(
            url=f'/tasks/{task_id}',
            params={"task_id": int(task_id)},
            json=get_fake_raw_target(
                title='test',
                description='test',
                status='done',
            ).model_dump()
        )

        assert resp.status_code == 200

    async def test_remove_task(self, authenticated_user_session):
        task_id = await TargetsDAO.find_all_raw_task(get_fake_raw_target(
            title='test',
            description='test',
            status='done',
        ))
        resp = await authenticated_user_session.delete(
            url=f'/tasks/{task_id}',
            params={
                "task_id": int(task_id),
            }
        )

        assert resp.status_code == 200
