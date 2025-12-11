import asyncio

from redis.asyncio import Redis

from .domain.use_cases import UseCases
from .service import BotService


async def main():
    redis = Redis(max_connections=20, decode_responses=True)
    bot_service = BotService(redis)
    use_cases = UseCases(redis)
    bot_service.configure(use_cases)
    try:
        await bot_service.run()
    finally:
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())
