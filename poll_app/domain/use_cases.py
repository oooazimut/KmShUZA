from typing import Dict, List, Optional
from .ports import PumpRepo, Receiver


class UseCases:
    def __init__(
        self,
        receiver: Receiver,
        pump_repo: Optional[PumpRepo] = None,
    ) -> None:
        self._receiver = receiver
        self._pump_repo = pump_repo

    async def receive_data(self) -> Dict[str, List]:
        return await self._receiver.receive()

    async def save_received(self, data):
        return await self._pump_repo.add_list(data)

    async def receive_and_save(self):
        data = await self.receive_data()
        if data:
            await self.save_received(data["pumps"])
