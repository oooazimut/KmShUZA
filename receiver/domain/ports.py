from typing import Protocol


class Receiver(Protocol):
    async def receive(self): ...


class PumpRepo(Protocol):
    async def add_list(self, data): ...
