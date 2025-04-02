from models import Item, Task
from repositories import get_conn
from repositories.products import get_prods_to_buy
from repositories.tasks import get_tasks

conn = get_conn()

items = get_prods_to_buy(conn)

for item_ in items:
    product = Item(
        item_id=item_[0],
        name=item_[1],
        is_done=item_[2],
        done_at=str(item_[3])
    )

    # print(f'{product.name} {product.done_at if product.is_done else "pendente"}')


tasks = get_tasks(conn)

conn.close()

for task in tasks:
    task_item = Task(
        item_id=task[0],
        name=task[1],
        description=task[2],
        is_done=task[3],
        done_at=str(task[4])
    )
    print(f'{task_item.name} {task_item.done_at if task_item.is_done else "pendente"}')
    print(f'    ({task_item.description if task_item.description else ""})')
