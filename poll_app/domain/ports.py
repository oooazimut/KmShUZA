from typing import Dict, Iterable, List, Protocol

from .entities import Pump


class Receiver(Protocol):
    async def receive(self) -> Dict[str, List]: ...


class PumpRepo(Protocol):
    async def add_list(self, data: Iterable[Pump]): ...
