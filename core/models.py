from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Pump:
    id: int
    is_working: bool = False
    pressure: float = 0
    runtime_minutes: int = 0
    timestamp: datetime = datetime.today()

    @property
    def runtime_hours(self):
        return int(self.runtime_minutes / 60)


@dataclass(frozen=True)
class Uza:
    is_active: bool
    selector: int
    permission: bool
