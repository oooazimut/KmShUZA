from ports import PumpRepo, Receiver

from logger import OnceLogger

once_logger = OnceLogger()


class UseCases:
    def __init__(self, receiver: Receiver, pump_repo: PumpRepo) -> None:
        self._receiver = receiver
        self._pump_repo = pump_repo

    @once_logger.log_exceptions_for_once
    async def receive_and_save(self):
        data = await self._receiver.receive()
        if data:
            await self._pump_repo.add_list(data["pumps"])
