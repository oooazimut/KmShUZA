from contextlib import asynccontextmanager
import aiosqlite as sq
import asyncio
from pathlib import Path


class SqliteConnFactory:
    def __init__(self, db_path) -> None:
        self._db_path = db_path
        self._conn: sq.Connection = None

    async def __aenter__(self) -> sq.Connection:
        self._conn = await sq.connect(self._db_path)
        self._conn.row_factory = sq.Row
        return self._conn

    async def __aexit__(self, exc_type, exc, tb):
        if self._conn:
            await self._conn.close()
            self._conn = None


class SqliteBaseRepo:
    def __init__(self, conn: sq.Connection) -> None:
        self._conn: sq.Connection = conn
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def _transaction(self):
        async with self._lock:
            try:
                await self._conn.execute("BEGIN")
                yield self._conn
                await self._conn.commit()
            except Exception:
                await self._conn.rollback()
                raise


async def init_db(db_path: Path, script: Path, conn: sq.Connection):
    with open(script, "r", encoding="utf-8") as file:
        await conn.executescript(file.read())
        await conn.commit()
