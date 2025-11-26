from datetime import date
from typing import Dict, Iterable, List

from domain.models import Pump

from .ports import DataReceiver, InfoPresenter, PumpRepo, UserRepo


class UseCases:
    def __init__(
        self,
        receiver: DataReceiver,
        pump_repo: PumpRepo,
        user_repo: UserRepo,
        presenter: InfoPresenter,
    ):
        self._receiver = receiver
        self._pump_repo = pump_repo
        self._user_repo = user_repo
        self._presenter = presenter

    async def receive_data(self) -> Dict:
        return await self._receiver.receive()

    def get_cache(self):
        return self._receiver.get_cache()

    async def get_from_storage_by_date(self, date: date) -> Iterable[Pump | None]:
        return await self._pump_repo.list_by_date(date)

    async def save_received_data(self, data: Iterable[Pump]) -> None:
        await self._pump_repo.save_list(data)

    async def save_user(self, user):
        await self._user_repo.add(user)

    async def get_user(self, id: int):
        await self._user_repo.get(id)

    async def present_curr_info(self, data: Dict):
        self._presenter.present_curr_info(data)

    async def present_archive_info(self, data: List):
        self._presenter.present_archive_info(data)
