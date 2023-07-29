from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path

from app.backend.targets.dao import TargetsDAO
from app.backend.targets.schemas import RawTarget, DetailedTarget, UpdatedTarget, DeletedTarget
from app.backend.users.dependencies import get_current_user
from app.backend.users.models import Users

router = APIRouter(
    prefix='/tasks',
    tags=['TASKS(TARGETS)'],
)


@router.post('')
async def new_task(raw_task: RawTarget, user: Users = Depends(get_current_user)) -> DetailedTarget:
    """Adds to db required basic task(target) info(raw_task). Return to the client more detailed task(target)"""

    user_id = user.id
    added_task_id = await TargetsDAO.add(
        user_id=user_id,
        status=raw_task.status,
        title=raw_task.title,
        description=raw_task.description,
    )
    res = await TargetsDAO.get_by_target_id(target_id=added_task_id)
    return res


@router.get('')
async def my_tasks(
        user: Users = Depends(get_current_user),
        limit: Annotated[
            int,
            Path(
                title="Limit for returning task",
                gt=-1
            ),
        ] = 20,
) -> list[DetailedTarget]:
    """Gets all specific user tasks(targets).
    Default it returns 20 tasks, but it's changeable on the client side and cannot be negative"""

    return await TargetsDAO.find_all_by_id(user.id, limit=limit)


@router.put('/{task_id}')
async def update_task(
        task_id: Annotated[int, Path(gt=0)],
        raw_target: RawTarget,
) -> UpdatedTarget:
    """Updates task and return task info with additional field (updated_at)"""

    updating_task_scheme_result = await TargetsDAO.update_user_task(task_id, raw_target)
    return updating_task_scheme_result


@router.delete('/{task_id}')
async def remove_task(
        task_id: Annotated[int, Path(gt=0)],
        user: Users = Depends(get_current_user),
) -> DeletedTarget:
    """Removes chosen task for specific user"""

    return await TargetsDAO.delete_task_by_task_id(task_id=task_id, user_id=user.id)
