import sqlite3 as sq
from dataclasses import asdict
from datetime import datetime
from typing import Dict

from domain.models import Pump, User


def pump_to_row(pump: Pump) -> Dict:
    result = asdict(pump)
    result["timestamp"] = result["timestamp"].isoformat()
    result["is_working"] = int(result["is_working"])
    result["emergency_mode"] = int(result["emergency_mode"])
    return result


def pump_from_row(row: sq.Row) -> Pump:
    return Pump(
        name=str(row["name"]),
        is_working=bool(row["is_working"]),
        pressure=row["pressure"],
        runtime=row["runtime"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        emergency_mode=bool(row["emergency_mode"]),
        # timestamp=row["timestamp"],
    )


def user_to_row(user: User) -> Dict:
    return asdict(user)


def user_from_row(row: sq.Row) -> User:
    return User(**row)
