from datetime import date
from typing import Iterable, Protocol

from core.models import Pump, Uza


class Receiver(Protocol):
    def receive_data(self) -> Iterable[Pump | Uza | None]: ...


class Repo(Protocol):
    def save_data(self, data: Iterable[Pump | Uza]): ...

    def get_pumps_by_date(self, date: date) -> Iterable[Pump | None]: ...
