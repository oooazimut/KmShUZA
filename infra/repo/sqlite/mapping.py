import sqlite3 as sq
from dataclasses import asdict
from datetime import datetime
from typing import Dict

from domain.models import Pump


def to_row(pump: Pump) -> Dict:
    result = asdict(pump)
    result["timestamp"] = result["timestamp"].isoformat()
    result["is_working"] = int(result["is_working"])
    return result


def from_row(row: sq.Row) -> Pump:
    return Pump(
        name=str(row["name"]),
        is_working=bool(row["is_working"]),
        pressure=row["pressure"],
        runtime_minutes=row["runtime_minutes"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        # timestamp=row["timestamp"],
    )
