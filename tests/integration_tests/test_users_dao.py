from app.backend.targets.schemas import RawTarget


class TestAuthenticatedUserDAOManipulations:
    """

class RawTarget(BaseModel):
    title: str = Field(max_length=150)
    description: str = Field(max_length=300)
    status: str = Field(default="new")
    """

    async def test_new_task(self, test_database_preparation, authenticated_user):
        session, fake_user = authenticated_user
        resp = await session.post(url='/tasks', json=RawTarget(**{
            "title": "qqqq",
            "description": "qweqwe",
            "status": "dodododo",
        }).model_dump())

        assert resp.status_code == 200
