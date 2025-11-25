from datetime import date
from typing import Iterable

from domain.models import Pump

from .ports import DataReceiver, PumpRepo, UserRepo


class UseCases:
    def __init__(
        self, receiver: DataReceiver, pump_repo: PumpRepo, user_repo: UserRepo
    ):
        self._receiver = receiver
        self._pump_repo = pump_repo
        self._user_repo = user_repo

    async def receive_data(self) -> Iterable:
        return await self._receiver.receive_data()

    async def get_from_storage_by_date(self, date: date) -> Iterable[Pump | None]:
        return await self._pump_repo.get_pumps_by_date(date)

    async def save_received_data(self, data: Iterable[Pump]) -> None:
        await self._pump_repo.save_pumps(data)

    async def save_user(self, user):
        await self._user_repo.save_user(user)

    def get_cached_models(self):
        return self._receiver.get_cache()
