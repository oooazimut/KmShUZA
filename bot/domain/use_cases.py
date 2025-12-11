from datetime import date
from typing import List
from bot.infra.cache_service import RedisCashe
from domain.entities import Pump, User
from redis.asyncio import Redis

from domain.ports import CacheGetter


class UseCases:
    def __init__(self, redis: Redis) -> None:
        self._user_repo = None
        self._pump_repo = None
        self._cache: CacheGetter = RedisCashe(redis)

    async def save_user(self, user: User) -> User:
        return user

    async def get_user(self, telegram_id: int) -> User | None:
        pass

    async def get_from_storage_by_date(self, date: date) -> List[Pump | None]:
        return list()

    async def get_cache(self):
        return self._cache.get()
