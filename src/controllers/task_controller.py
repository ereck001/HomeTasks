from typing import Optional

from fastapi import APIRouter, Query
from fastapi.responses import UJSONResponse

from models import Task, TaskBase, TaskRaw
from repositories import get_conn
from repositories.tasks import (add_task, delete_task, get_task_by_id,
                                get_tasks, update_task)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def list_tasks(
        not_done_only: Optional[bool] = Query(None, alias="not_done_only"),
        done_only: Optional[bool] = Query(None, alias="done_only")):

    tasks = []
    conn = get_conn()
    items = get_tasks(conn, not_done_only, done_only)
    conn.close()

    for i in items:
        task = Task(
            item_id=i[0],
            name=i[1],
            description=i[2],
            is_done=bool(i[3]),
            done_at=str(i[4])
        )
        tasks.append(task.model_dump())

    return {"Tasks": tasks}


@router.get("/{task_id}")
async def get_task(task_id: int):
    conn = get_conn()
    task = get_task_by_id(conn, task_id)
    conn.close()

    if (not task):
        return {"erro": f"Tarefa {task_id} não encontrada"}

    task_item = Task(
        item_id=task[0],
        name=task[1],
        description=task[2],
        is_done=bool(task[3]),
        done_at=str(task[4])
    )

    return {"Tarefa": task_item}


@router.post("/")
async def add(task: TaskRaw):
    if task.name.strip() == "":
        return UJSONResponse({'Erro': 'O nome é obrigatório'}, 400)
    conn = get_conn()
    task_name = add_task(conn, task.name, task.description)
    conn.close()

    return {'Adicionado': task_name}


@router.put("/{task_id}")
async def update(task_id: int, task: TaskBase):
    task_to_update = Task(
        item_id=task_id,
        name=task.name,
        description=task.description,
        is_done=task.done_at != None,
        done_at=task.done_at
    )

    # if task_to_update.name.strip() == '' and \
    #         task_to_update.description.strip() == '' and task_to_update.done_at == None:
    #     return UJSONResponse({'Erro': 'Atualize ao menos um atributo'}, 400)

    conn = get_conn()

    try:
        task_name = update_task(conn, task_to_update)

    except ValueError as err:
        return UJSONResponse({'Erro': str(err)}, 400)

    conn.close()

    return {'Atualizado': task_name}


@router.delete("/{task_id}")
async def delete(task_id: int):
    conn = get_conn()

    try:
        id = delete_task(conn, task_id)

    except ValueError as err:
        return UJSONResponse({'Erro': str(err)}, 400)

    conn.close()

    return {'Excluído': id}
