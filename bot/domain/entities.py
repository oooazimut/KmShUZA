from dataclasses import asdict, dataclass, field
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass(frozen=True)
class Pump:
    name: str
    is_working: bool = False
    pressure: float = 0
    runtime: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    emergency_mode: bool = False
    pressure_alert: bool = False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pump):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def as_dict(self):
        result = asdict(self)
        result["timestamp"] = result["timestamp"].isoformat()
        return result


@dataclass(frozen=True)
class Uza:
    number: int
    is_active: bool
    selector: int
    permission: bool
    break_alert: bool

    def as_dict(self):
        return asdict(self)


@dataclass()
class User:
    name: str
    password: str = ""
    telegram_id: int | None = None

    def set_password(self, passwd):
        self.password = generate_password_hash(passwd)

    def check_password(self, passwd):
        return check_password_hash(self.password, passwd)
