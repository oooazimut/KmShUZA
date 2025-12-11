import json
from redis.asyncio import Redis

from domain.entities import Pump
from domain.ports import CacheGetter


class RedisCashe(CacheGetter):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def get(self):
        if (raw := await self._redis.get("modbus:latest")) is None:
            return None

        return [Pump(**item) for item in json.loads(raw)]
