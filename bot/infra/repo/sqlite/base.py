import asyncio
from contextlib import asynccontextmanager

import aiosqlite as sq


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
