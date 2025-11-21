from datetime import date
from typing import Iterable

from domain.models import Pump

from .ports import DataReceiver, PumpRepo


class UseCases:
    def __init__(self, receiver: DataReceiver, repo: PumpRepo):
        self.receiver = receiver
        self.repo = repo

    def receive_data(self) -> Iterable:
        return self.receiver.receive_data()

    def get_from_storage_by_date(self, date: date) -> Iterable[Pump | None]:
        return self.repo.get_pumps_by_date(date)

    def save_received_data(self, data: Iterable[Pump]) -> None:
        self.repo.save_pumps(data)
