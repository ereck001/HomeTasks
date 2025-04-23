import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection

from ..authentication import hash_password
from ..functions import save_log

load_dotenv()


def get_conn() -> connection:
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


def create_tables(conn: connection):
    admin_password = os.getenv("ADM_PASS")

    if not admin_password:
        raise Exception('Configurar a variavel de ambiente ADM_PASS')

    sql1 = """
        CREATE TABLE IF NOT EXISTS Tasks(
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            description TEXT,
            isDone BOOLEAN NOT NULL,
            doneAt DATE
        );
    """

    sql2 = """
        CREATE TABLE IF NOT EXISTS PurchasedProducts(
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            isPurchased BOOLEAN NOT NULL,
            doneAt DATE
        );
    """

    sql3 = """
        CREATE TABLE IF NOT EXISTS Roles (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50)  NOT NULL UNIQUE
        );
    """

    sql4 = """
        INSERT INTO Roles (id, name)
        VALUES
            ( 1, 'admin'),
            ( 2, 'user')
        ON CONFLICT (id) DO NOTHING;
    """

    sql5 = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            password VARCHAR(150) NOT NULL,
            role_id INTEGER NOT NULL REFERENCES roles(id)
        );
    """

    sql6 = """
        INSERT INTO Users(name, password, role_id)
        SELECT %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM Users WHERE name = 'admin'
        );
    """

    try:
        with conn.cursor() as cursor:

            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql3)

            cursor.execute(sql4)
            cursor.execute(sql5)
            cursor.execute(sql6, ['admin', hash_password(admin_password), 1])

            conn.commit()

    except Exception as e:
        conn.rollback()
        save_log("❌ Erro ao criar tabelas ou inserir dados:" + str(e))
        raise
