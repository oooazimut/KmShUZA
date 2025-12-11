import asyncio
import logging

from config import settings
from domain import UseCases
from infra.bot import BotService
from infra.logger import configure_logging
from infra.receiver.modbus import ModbusReceiver
from infra.repo.sqlite import SqlitePumpRepo, SqliteUserRepo, create_conn, init_db
from infra.scheduler import SchedulerService


async def main():
    try:
        conn = await create_conn()
        await init_db(conn)

        use_cases = UseCases(
            ModbusReceiver(settings.modbus),
            SqlitePumpRepo(conn),
            SqliteUserRepo(conn),
        )

        bot_service = BotService()
        bot_service.configure(use_cases)
        await bot_service.run()

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
