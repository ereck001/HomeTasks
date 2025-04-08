from psycopg2.extensions import connection

from models import User

TABLE_NAME = 'Users'


def get_user_by_name(conn: connection, name: str) -> tuple | None:

    sql = f'SELECT * FROM {TABLE_NAME} WHERE Name = %s'
    cursor = conn.cursor()
    cursor.execute(sql, [name])

    item = cursor.fetchone()
    cursor.close()
    return item


def get_user_by_id(conn: connection, id: int) -> tuple | None:

    sql = f'SELECT * FROM {TABLE_NAME} WHERE id = %s'
    cursor = conn.cursor()
    cursor.execute(sql, [id])

    item = cursor.fetchone()
    cursor.close()
    return item


def add_user(conn: connection, name: str, password: str) -> str:
    cursor = conn.cursor()
    sql = f"""
            INSERT INTO {TABLE_NAME} (Name, Password, role_id)
            VALUES
                ( %s, %s, 2);
            """
    cursor.execute(sql, [name, password])
    conn.commit()
    cursor.close()
    return name


# def update_user(conn: connection, task: Task) -> str:
#     cursor = conn.cursor()

#     sql = f"UPDATE {TABLE_NAME} SET "
#     sql += "name=%s, " if task.name.strip() != "" else ""
#     sql += "description=%s, "if task.description.strip() != "" else ""
#     sql += "isDone=%s, "
#     sql += "doneAt=%s  "
#     sql += "WHERE id=%s;"

#     vars_list = []

#     if task.name.strip() != "":
#         vars_list.append(task.name,)
#     if task.description.strip() != "":
#         vars_list.append(task.description,)
#     vars_list.append(task.is_done,)  # type: ignore
#     vars_list.append(task.done_at,)  # type: ignore
#     vars_list.append(task.item_id)  # type: ignore

#     cursor.execute(sql, vars_list)
#     affected_rows = cursor.rowcount
#     conn.commit()
#     cursor.close()

#     if affected_rows == 0:
#         raise ValueError(f"Tarefa com ID {task.item_id} não encontrada")

#     return task.name


# def delete_user(conn: connection, id: int) -> int:
#     cursor = conn.cursor()
#     sql = f'DELETE FROM {TABLE_NAME} WHERE id = %s '

#     cursor.execute(sql, [id])
#     affected_rows = cursor.rowcount
#     conn.commit()
#     cursor.close()

#     if affected_rows == 0:
#         raise ValueError(f"Tarefa com ID {id} não encontrada")

#     return id
