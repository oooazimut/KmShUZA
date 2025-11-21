import json
from dataclasses import asdict
from pathlib import Path
import sqlite3 as sq
from datetime import date, datetime
from typing import Iterable

from domain.models import Pump


def adapt_pump(pump: Pump) -> str:
    data = asdict(pump)
    data["timestamp"] = data["timestamp"].isoformat()
    return json.dumps(data)


def convert_pump(pump: bytes) -> Pump:
    data = json.loads(pump)
    data["timestamp"] = datetime.fromisoformat(data["timestamp"])
    # del data["id"]
    return Pump(**data)


class SqlitePumpRepo:
    def _connection(self):
        pass

    def create_db(self, db_name: str, script_name: Path):
        with open(script_name, "r", encoding="utf-8") as file:
            script = file.read()

        with sq.connect(db_name) as con:
            con.executescript(script)

    def save_pumps(self, data: Iterable[Pump]) -> Iterable[int]:
        return []

    def get_pumps_by_date(self, date: date) -> Iterable[Pump | None]:
        return []
