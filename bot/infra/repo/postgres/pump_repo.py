from datetime import date, timedelta
from typing import List

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from domain.entities import Pump
from domain.ports import PumpRepo

from .base_repo import PGBaseRepo


class PGPumpRepo(PGBaseRepo, PumpRepo):
    def __init__(self, pool: AsyncConnectionPool) -> None:
        super().__init__(pool)
        self.row_factory = class_row(Pump)

    async def add_list(self, data: List[Pump]):
        pumps = []
        query = """
            INSERT INTO pumps (name, is_working, pressure, runtime, emergency_mode, pressure_alert)
            VALUES (%(name)s, %(is_working)s, %(pressure)s, %(runtime)s, %(emergency_mode)s, %(pressure_alert)s)
            RETURNING name, is_working, pressure, runtime, emergency_mode, pressure_alert, timestamp
        """
        for pump in data:
            pumps.append(await self._fetchone(query, pump.as_dict()))

        return pumps

    async def list_by_date(self, target_date: date):
        end = target_date + timedelta(days=1)
        stmt = """
        SELECT name, is_working, pressure, runtime, timestamp, emergency_mode, pressure_alert
        FROM pumps
        WHERE timestamp >= %s AND timestamp < %s;"""
        return await self._fetchall(stmt, (target_date, end))
