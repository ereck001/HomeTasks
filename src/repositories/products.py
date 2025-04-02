from psycopg2.extensions import connection


def get_prods_to_buy(conn: connection) -> list[tuple]:
    # conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM PurchasedProducts')

    items = cursor.fetchall()
    # conn.close()
    if not items:
        return []

    return items
