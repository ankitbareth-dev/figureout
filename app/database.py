import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import DictRow, dict_row

load_dotenv()


def get_connection() -> psycopg.Connection[DictRow]:
    database_url = os.getenv("DATABASE_URL")

    if database_url is None:
        raise RuntimeError("DATABASE_URL is not configured")

    return psycopg.Connection[DictRow].connect(
        database_url,
        row_factory=dict_row,
    )