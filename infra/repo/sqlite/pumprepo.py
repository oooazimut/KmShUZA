import asyncio
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
from typing import Iterable

import aiosqlite as sq

from domain.models import Pump

from .mapping import from_row, to_row


class SqlitePumpRepo:
    def __init__(self, db_path: str, init_script: str) -> None:
        self._db_path = Path(db_path)
        self._init_script: Path = Path(init_script)
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

    async def create_db(self):
        with open(self._init_script, "r", encoding="utf-8") as file:
            script = file.read()

        async with self._transaction() as conn:
            await conn.executescript(script)

    async def save_pumps(self, pumps: Iterable[Pump]) -> Iterable[Pump]:
        saved_pumps = []
        query = """INSERT INTO pumps (name, is_working, pressure, runtime, emergency_mode)
                   VALUES (:name, :is_working, :pressure, :runtime, :emergency_mode)
                   RETURNING *
                """
        async with self._transaction() as conn:
            for pump in pumps:
                cursor = await conn.execute(query, to_row(pump))
                saved_pumps.append(from_row(await cursor.fetchone()))

        return saved_pumps

    async def get_pumps_by_date(self, date: date) -> Iterable[Pump | None]:
        query = "SELECT * FROM pumps WHERE DATE(timestamp) = ?"
        async with self._transaction() as conn:
            cursor = await conn.execute(query, [date.isoformat()])
            rows = await cursor.fetchall()

        return [from_row(row) for row in rows]
