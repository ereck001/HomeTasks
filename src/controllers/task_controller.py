from fastapi import APIRouter

from models import Task
from repositories import get_conn
from repositories.tasks import get_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def list_tasks():
    tasks = []
    conn = get_conn()
    items = get_tasks(conn)

    for task in items:
        task = Task(
            item_id=task[0],
            name=task[1],
            description=task[2],
            is_done=task[3],
            done_at=str(task[4])
        )
        tasks.append(task.model_dump())

    return {"Tasks": tasks}
