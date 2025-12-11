from dataclasses import dataclass
from domain.entities import User


@dataclass
class TgUser(User):
    telegram_id: int = None
