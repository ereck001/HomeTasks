from psycopg2.extensions import connection

from models import Item

TABLE_NAME = 'PurchasedProducts'


def get_prods_to_buy(
        conn: connection, only_active: bool | None = False,  only_not_active: bool | None = False) -> list[tuple]:

    cursor = conn.cursor()

    sql = f'SELECT * FROM {TABLE_NAME} '

    if only_active:
        sql += 'WHERE IsPurchased = False '

    if only_not_active and not only_active:
        sql += 'WHERE IsPurchased = True ORDER BY DoneAt DESC'

    cursor.execute(sql)

    items = cursor.fetchall()
    cursor.close()

    if not items:
        return []

    return items


def get_produduct_by_id(conn: connection, id: int) -> tuple | None:

    sql = f'SELECT * FROM {TABLE_NAME} WHERE id = %s'
    cursor = conn.cursor()
    cursor.execute(sql, [id])

    item = cursor.fetchone()
    cursor.close()
    return item


def add_product(conn: connection, name: str) -> str:
    cursor = conn.cursor()
    sql = f"""
            INSERT INTO {TABLE_NAME} (name,  isPurchased, doneAt)
            VALUES
                ( %s, FALSE, NULL);
            """
    cursor.execute(sql, [name])
    conn.commit()
    cursor.close()
    print(sql)
    return name


def update_product(conn: connection, product: Item) -> str:
    cursor = conn.cursor()
    sql = f"""
            UPDATE {TABLE_NAME} SET 
            name=%s,
            isPurchased=%s,
            doneAt=%s
            WHERE id=%s;
            """

    vars_list = [product.name, product.is_done,
                 product.done_at, product.item_id]

    if product.name.strip() == "":
        sql = f"""
            UPDATE {TABLE_NAME} SET 
            isPurchased=%s,
            doneAt=%s
            WHERE id=%s;
            """

        vars_list = [product.is_done, product.done_at, product.item_id]

    cursor.execute(sql, vars_list)
    affected_rows = cursor.rowcount  # Número de linhas alteradas
    conn.commit()
    cursor.close()

    if affected_rows == 0:
        raise ValueError(f"Produto com ID {product.item_id} não encontrado")

    return product.name


def delete_product(conn: connection, id: int) -> int:
    cursor = conn.cursor()
    sql = f'DELETE FROM {TABLE_NAME} WHERE id = %s '

    cursor.execute(sql, [id])
    affected_rows = cursor.rowcount  # Número de linhas excluídas
    conn.commit()
    cursor.close()

    if affected_rows == 0:
        raise ValueError(f"Produto com ID {id} não encontrado")

    return id
