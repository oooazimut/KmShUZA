import asyncio

from redis.asyncio import Redis

from config import settings
from infra.repo.postgres.pool import create_pool
from infra.repo.postgres.pump_repo import PGPumpRepo
from infra.repo.postgres.user_repo import PGUserRepo
from logger import configure_logging

from domain.use_cases import UseCases
from service import BotService


async def main():
    configure_logging("bot")
    pool = create_pool(
        user=settings.pg.user,
        password=settings.pg.passw.get_secret_value(),
    )
    await pool.open()
    redis = Redis(max_connections=20, decode_responses=True)
    bot_service = BotService(redis)
    use_cases = UseCases(redis, user_repo=PGUserRepo(pool), pump_repo=PGPumpRepo(pool))
    bot_service.configure(use_cases)
    try:
        await bot_service.run()
    finally:
        await redis.aclose()
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
