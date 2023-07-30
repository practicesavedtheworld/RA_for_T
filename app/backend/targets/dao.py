import datetime
import logging
from typing import Any, Callable, ParamSpec, TypeAlias

from pydantic import TypeAdapter
from sqlalchemy import Result, select, update

from app.backend.app_logging import create_logger
from app.backend.dao.dao import BaseDAO
from app.backend.targets.exceptions import NoTargetFound
from app.backend.targets.models import Targets
from app.backend.targets.schemas import DetailedTarget, RawTarget, UpdatedTarget

RESULT_FROM_DB: TypeAlias = Any | None
P = ParamSpec("P")
targets_dao_logger = create_logger(
    loger_name="targets_dao_logger",
    level=logging.WARNING,
)


class TargetsDAO(BaseDAO):
    current_model = Targets

    @staticmethod
    def database_result_validator(critical: bool = False) -> Callable:
        """See that the returned object from the database is useless to the user.
        If it is, log that or throw an exception, depends on critical attribute"""

        def validator(dao_func: Callable) -> Callable[P, RESULT_FROM_DB]:
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> RESULT_FROM_DB:
                dao_func_result: RESULT_FROM_DB = await dao_func(*args, **kwargs)
                if not RESULT_FROM_DB and critical:
                    raise NoTargetFound
                elif not RESULT_FROM_DB:
                    targets_dao_logger.warning(
                        "User requests object that is not exist or its already deleted"
                    )
                return dao_func_result

            return wrapper

        return validator

    @classmethod
    @database_result_validator(critical=True)
    async def update_user_task(
        cls, task_id: int, raw_target: RawTarget
    ) -> UpdatedTarget:
        """Update task selected by client and return task with updating fields"""

        async with cls.session_ as session:
            update_query = (
                update(cls.current_model)
                .where(Targets.id == task_id)
                .values(
                    title=raw_target.title,
                    description=raw_target.description,
                    status=raw_target.status,
                    updated_at=datetime.datetime.utcnow(),
                )
                .returning(
                    Targets.id,
                    Targets.title,
                    Targets.description,
                    Targets.status,
                    Targets.created_at,
                    Targets.updated_at,
                )
            )
            update_query_result = await session.execute(update_query)
            await session.commit()

            #  Set Result as a pydantic schemas
            adapter: UpdatedTarget | None = TypeAdapter(UpdatedTarget).validate_python(
                update_query_result.mappings().one_or_none()
            )

            return adapter

    @classmethod
    @database_result_validator(critical=True)
    async def get_by_target_id(cls, target_id: int) -> DetailedTarget:
        """Select specific fields of target for specific user.
        Required by assignment:
        id
        title
        description
        status
        created_at
        """

        async with cls.session_ as session:
            select_query = select(
                Targets.id,
                Targets.title,
                Targets.description,
                Targets.status,
                Targets.created_at,
            ).filter_by(id=target_id)
            query_result: Result = await session.execute(select_query)

            #  Set Result as a  pydantic schemas
            adapter: DetailedTarget | None = TypeAdapter(
                DetailedTarget
            ).validate_python(query_result.mappings().one_or_none())
            return adapter

    @classmethod
    async def find_all_by_id(cls, id_: int, limit: int = None) -> list[DetailedTarget]:
        """Selects all tasks(targets) for a specific user.
        As a result, it includes only 5 fields required by the assignment"""

        async with cls.session_ as session:
            query = (
                select(
                    Targets.id,
                    Targets.title,
                    Targets.description,
                    Targets.status,
                    Targets.created_at,
                )
                .where(Targets.user_id == id_)
                .limit(limit)
            )
            query_result: Result = await session.execute(query)

            #  Set Result as a list of pydantic schemas
            adapter = TypeAdapter(list[DetailedTarget]).validate_python(
                query_result.mappings().all()
            )
            return adapter
