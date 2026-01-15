from datetime import date
from typing import Dict, Iterable, List, Protocol

from domain.entities import Pump, User, Uza


class DataReceiver(Protocol):
    async def receive(self) -> Dict[str, List[Pump | Uza]]: ...
    def get_cache(self) -> Dict[str, List]: ...


class PumpRepo(Protocol):
    async def add_list(self, data: Iterable[Pump]): ...
    async def list_by_date(self, date: date) -> List[Pump]: ...


class UserRepo(Protocol):
    async def add(self, user: User) -> User: ...

    """
    бросает исключение UserAlreadyExists,
    если пользователь с таким именем существует
    """

    async def get(self, id: int) -> User | None: ...

    async def get_by_login(self, login: str) -> User: ...

    async def get_by_tg_id(self, tg_id: int) -> User: ...

    async def remove_by_login(self, login: str): ...


class InfoPresenter(Protocol):
    def present_curr_info(self, data: Dict[str, List]): ...
    def present_archive_info(self, data: list[Pump]): ...


class CacheSetter(Protocol):
    async def set(self, data): ...


class CacheGetter(Protocol):
    async def get(self): ...
