from .ports import PumpRepo, Receiver


class UseCases:
    def __init__(self, receiver: Receiver, pump_repo: PumpRepo) -> None:
        self._receiver = receiver
        self._pump_repo = pump_repo

    async def receive_data(self):
        return self._receiver.receive()

    async def save_received_to_db(self, data):
        return self._pump_repo.add_list(data)
