import asyncio
import logging

from logger import configure_logging
from config import settings
from poll_app.infra.repo.postgres.pool import create_pool
from poll_app.infra.repo.postgres.pump_repo import PGPumpRepo

from .domain.use_cases import UseCases
from .infra.receiver.modbus import ModbusReceiver


async def main():
    pool = create_pool()
    configure_logging()
    try:
        await pool.open()
        repo = PGPumpRepo(pool)
        use_cases = UseCases(ModbusReceiver(settings.modbus), repo)
        while True:
            await use_cases.receive_and_save()
            await asyncio.sleep(5)
    finally:
        await pool.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
