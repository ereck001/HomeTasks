from psycopg2.extensions import connection


def get_tasks(conn: connection) -> list[tuple]:
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Tasks')

    items = cursor.fetchall()
    if not items:
        return []

    return items
