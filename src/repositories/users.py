from psycopg2.extensions import connection

# from models import User

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
