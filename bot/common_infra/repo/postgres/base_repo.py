import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

import psycopg
from psycopg.rows import AsyncRowFactory
from psycopg_pool import AsyncConnectionPool

from config import settings


class PGBaseRepo:
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool
        self.row_factory: AsyncRowFactory | None = None

    @asynccontextmanager
    async def _transaction(self):
        async with self._pool.connection() as conn:
            async with conn.transaction():
                yield conn

    @asynccontextmanager
    async def _cursor(self):
        async with self._transaction() as conn:
            if self.row_factory:
                async with conn.cursor(row_factory=self.row_factory) as cur:
                    yield cur
            else:
                async with conn.cursor() as cur:
                    yield cur

    async def _execute(self, stmt, params=None):
        async with self._cursor() as cur:
            await cur.execute(stmt, params)

    async def _fetchone(self, stmt, params=None):
        async with self._cursor() as cur:
            await cur.execute(stmt, params)
            return await cur.fetchone()

    async def _fetchall(self, stmt, params=None):
        async with self._cursor() as cur:
            await cur.execute(stmt, params)
            return await cur.fetchall()


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
                sql: str = file.read()
                await cur.execute(sql)
        await conn.commit()


if __name__ == "__main__":
    asyncio.run(init_db())
