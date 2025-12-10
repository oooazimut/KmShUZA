from typing import Dict, List, Protocol


class Receiver(Protocol):
    async def receive(self) -> Dict[str, List]: ...


class PumpRepo(Protocol):
    async def add_list(self, data): ...
