from datetime import date
from typing import Iterable

from domain.models import Pump
from domain.ports import PumpRepo

from .base import SqliteBaseRepo
from .mapping import pump_from_row, pump_to_row


class SqlitePumpRepo(SqliteBaseRepo, PumpRepo):
    async def save_list(self, pumps: Iterable[Pump]) -> Iterable[Pump]:
        saved_pumps = []
        query = """INSERT INTO pumps (name, is_working, pressure, runtime, emergency_mode, pressure_alert)
                   VALUES (:name, :is_working, :pressure, :runtime, :emergency_mode, :pressure_alert)
                   RETURNING *
                """
        async with self._transaction() as conn:
            for pump in pumps:
                cursor = await conn.execute(query, pump_to_row(pump))
                saved_pumps.append(pump_from_row(await cursor.fetchone()))

        return saved_pumps

    async def list_by_date(self, date: date) -> Iterable[Pump | None]:
        query = "SELECT * FROM pumps WHERE DATE(timestamp) = ?"
        async with self._transaction() as conn:
            cursor = await conn.execute(query, [date.isoformat()])
            rows = await cursor.fetchall()

        return [pump_from_row(row) for row in rows]
