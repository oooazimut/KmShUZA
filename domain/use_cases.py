from datetime import date
from typing import Dict, Iterable

from domain.models import Pump

from .ports import DataReceiver, PumpRepo


class UseCases:
    def __init__(self, receiver: DataReceiver, repo: PumpRepo):
        self._receiver = receiver
        self._repo = repo
        self._cache: Dict | None = None

    async def receive_data(self) -> Iterable:
        return await self._receiver.receive_data()

    async def get_from_storage_by_date(self, date: date) -> Iterable[Pump | None]:
        return await self._repo.get_pumps_by_date(date)

    async def save_received_data(self, data: Iterable[Pump]) -> None:
        await self._repo.save_pumps(data)

    def cache_models(self, models: Dict):
        self._cache = models

    def get_cached_models(self):
        return self._cache
