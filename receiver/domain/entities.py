from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Pump:
    name: str
    is_working: bool = False
    pressure: float = 0
    runtime: int = 0
    timestamp: datetime = datetime.today()
    emergency_mode: bool = False
    pressure_alert: bool = False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pump):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(frozen=True)
class Uza:
    number: int
    is_active: bool
    selector: int
    permission: bool
    break_alert: bool
