from datetime import date
from typing import Iterable, Protocol

from domain.models import Pump, Uza, User


class DataReceiver(Protocol):
    async def receive(self) -> Iterable[Pump | Uza | None]: ...
    async def get_cache(self) -> Iterable[Pump | Uza | None]: ...


class PumpRepo(Protocol):
    async def save_list(self, data: Iterable[Pump]): ...
    async def list_by_date(self, date: date) -> Iterable[Pump | None]: ...


class UserRepo(Protocol):
    async def add(self, user: User) -> User: ...

    """
    бросает исключение UserAlreadyExists,
    если пользователь с таким именем существует
    """

    async def get(self, id: int) -> User | None: ...
