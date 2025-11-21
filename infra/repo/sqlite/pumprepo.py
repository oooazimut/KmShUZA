from datetime import date
from typing import Iterable

from domain.models import Pump


class SqlitePumpRepo:
    def save_pumps(self, data: Iterable[Pump]) -> Iterable[int]:
        return []

    def get_pumps_by_date(self, date: date) -> Iterable[Pump | None]:
        return []
