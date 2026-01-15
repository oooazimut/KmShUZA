from typing import Iterable

from domain.entities import Pump
from domain.ports import PumpRepo
from infra.repo.mapping import pump_from_row, pump_to_row

from .base import SqliteBaseRepo


class SqlitePumpRepo(SqliteBaseRepo, PumpRepo):
    async def add_list(self, pumps: Iterable[Pump]) -> Iterable[Pump]:
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
