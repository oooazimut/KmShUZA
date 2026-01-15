from datetime import date
from typing import Dict, Iterable, Optional

from domain.models import Pump

from .ports import CacheService, DataReceiver, PumpRepo, UserRepo


class UseCases:
    def __init__(
        self,
        receiver: Optional[DataReceiver] = None,
        pump_repo: Optional[PumpRepo] = None,
        user_repo: Optional[UserRepo] = None,
    :
        self._receiver = receiver
        self._pump_repo = pump_repo
        self._user_repo = user_repo

    async def receive_data(self) -> Dict:
        return await self._receiver.receive()

    def get_cache(self):
        return self._receiver.get_cache()

    async def get_from_storage_by_date(self, date: date) -> Iterable[Pump | None]:
        return await self._pump_repo.list_by_date(date)

    async def save_received(self, data: Iterable[Pump]) -> None:
        return await self._pump_repo.save_list(data)

    async def save_user(self, user):
        return await self._user_repo.add(user)

    async def get_user(self, id: int):
        return await self._user_repo.get(id)
