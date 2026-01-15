from datetime import date
from typing import List
from bot.infra.cache_service import RedisCashe
from domain.entities import Pump, User
from redis.asyncio import Redis
from domain.ports import CacheGetter, PumpRepo, UserRepo


class UseCases:
    def __init__(self, redis: Redis, user_repo: UserRepo, pump_repo: PumpRepo) -> None:
        self._user_repo = user_repo
        self._pump_repo = pump_repo
        self._cache: CacheGetter = RedisCashe(redis)

    async def save_user(self, user: User) -> User:
        return await self._user_repo.add(user)

    async def get_user(self, key: str | int) -> User | None:
        if isinstance(key, str):
            return await self._user_repo.get_by_login(key)
        else:
            return await self._user_repo.get_by_tg_id(key)

    async def get_pumps_from_storage_by_date(self, target_date: date) -> List[Pump]:
        return await self._pump_repo.list_by_date(target_date)

    def get_cache(self):
        return self._cache.get()
