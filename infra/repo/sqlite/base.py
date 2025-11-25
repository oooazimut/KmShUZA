from contextlib import asynccontextmanager
import aiosqlite as sq
import asyncio
from pathlib import Path


class BaseRepo:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._conn: sq.Connection | None = None
        self._lock = asyncio.Lock()

    async def connect(self):
        self._conn = await sq.connect(self._db_path)
        self._conn.row_factory = sq.Row

    async def close_conn(self):
        if self._conn is not None:
            await self._conn.close()
            self._conn = None

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


async def init_db(db_path: Path, script: Path):
    repo = BaseRepo(db_path=db_path)
    await repo.connect()
    try:
        with open(script, "r", encoding="utf-8") as file:
            await repo._conn.executescript(file.read())
    finally:
        await repo.close_conn()
