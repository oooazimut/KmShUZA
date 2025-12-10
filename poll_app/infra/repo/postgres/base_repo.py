from config import settings
from contextlib import asynccontextmanager
from pathlib import Path

import psycopg
from psycopg_pool import AsyncConnectionPool


class PGBaseRepo:
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    @asynccontextmanager
    async def _transaction(self):
        async with self._pool.connection() as conn:
            async with conn.transaction():
                yield conn


async def init_db():
    script_path = Path(__file__).resolve().parent / "pg_table.sql"
    user = settings.pg.migrator
    passwd = settings.pg.migrator_passw.get_secret_value()
    host = settings.pg.host
    db = settings.pg.db_name

    async with await psycopg.AsyncConnection.connect(
        f"postgresql://{user}:{passwd}@{host}/{db}"
    ) as conn:
        async with conn.cursor() as cur:
            with open(script_path, "r", encoding="utf-8") as file:
                sql = file.read()
                await cur.execute(sql)
        await conn.commit()
