from datetime import date
from typing import Iterable, Protocol

from domain.models import Pump, Uza


class DataReceiver(Protocol):
    async def receive_data(self) -> Iterable[Pump | Uza | None]: ...


class PumpRepo(Protocol):
    async def create_db(self, db_name: str, script: str): ...
    async def save_pumps(self, data: Iterable[Pump]): ...
    async def get_pumps_by_date(self, date: date) -> Iterable[Pump | None]: ...
