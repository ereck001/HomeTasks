import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection

from models import Item

load_dotenv()


def get_conn() -> connection:
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


def get_prods_to_buy():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM PurchasedProducts')

    item_ = cursor.fetchone()

    if not item_:
        return

    product = Item(
        item_id=item_[0],
        name=item_[1],
        is_done=item_[2],
        done_at=str(item_[3])
    )

    print(product.done_at)
    conn.close()
