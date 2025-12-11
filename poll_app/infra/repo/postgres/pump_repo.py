from typing import List

from psycopg.rows import class_row
from .base_repo import PGBaseRepo
from poll_app.domain.ports import PumpRepo
from domain.entities import Pump


class PGPumpRepo(PGBaseRepo, PumpRepo):
    async def add_list(self, data: List[Pump]):
        pumps = []
        async with self._transaction() as conn:
            async with conn.cursor(row_factory=class_row(Pump)) as cur:
                query = """
                    INSERT INTO pumps (name, is_working, pressure, runtime, emergency_mode, pressure_alert)
                    VALUES (%(name)s, %(is_working)s, %(pressure)s, %(runtime)s, %(emergency_mode)s, %(pressure_alert)s)
                    RETURNING name, is_working, pressure, runtime, emergency_mode, pressure_alert, timestamp
                """
                for pump in data:
                    await cur.execute(query, pump.as_dict())
                    pumps.append(await cur.fetchone())

            return pumps
