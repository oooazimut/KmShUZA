from datetime import date
from typing import Iterable

from core.models import Pump, Uza

from .ports import Receiver, Repo


class UseCases:
    def __init__(self, receiver: Receiver, repo: Repo):
        self.receiver = receiver
        self.repo = repo

    def receive_data(self) -> Iterable:
        return self.receiver.receive_data()

    def get_from_storage_by_date(self, date: date) -> Iterable[Pump]:
        return self.repo.get_pumps_by_date(date)

    def save_received_data(self, data: Iterable[Pump | Uza]) -> None:
        self.repo.save_data(data)
