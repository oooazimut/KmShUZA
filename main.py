import asyncio
import logging
from config import settings
from domain.use_cases import UseCases
from infra.bot.service import BotService
from infra.logger import configure_logging
from infra.receiver.modbus.modbus_receiver import ModbusReceiver
from infra.repo.sqlite import create_conn, init_db
from infra.repo.sqlite.pumprepo import SqlitePumpRepo
from infra.repo.sqlite.user_repo import SqliteUserRepo
from infra.scheduler.service import SchedulerService


async def main():
    try:
        configure_logging(logging.WARNING)
        conn = await create_conn()
        await init_db(conn)

        use_cases = UseCases(
            ModbusReceiver(settings.modbus),
            SqlitePumpRepo(conn),
            SqliteUserRepo(conn),
        )

        scheduler_service = SchedulerService()
        scheduler_service.configure(use_cases)
        scheduler_service.run()

        bot_service = BotService()
        bot_service.configure(use_cases)
        await bot_service.run()

    finally:
        scheduler_service.stop()
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
