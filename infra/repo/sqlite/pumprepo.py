import sqlite3 as sq
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Iterable

from domain.models import Pump

from .mapping import from_row, to_row


class SqlitePumpRepo:
    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)

    @contextmanager
    def _transaction(self):
        conn = sq.connect(
            self.db_path, detect_types=sq.PARSE_DECLTYPES | sq.PARSE_COLNAMES
        )
        conn.row_factory = sq.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_db(self, db_name: str, script_name: Path):
        with open(script_name, "r", encoding="utf-8") as file:
            script = file.read()

        with self._transaction() as conn:
            conn.executescript(script)

    def save_pumps(self, pumps: Iterable[Pump]) -> Iterable[Pump]:
        saved_pumps = []
        query = """INSERT INTO pumps (name, is_working, pressure, runtime_minutes)
                   VALUES (:name, :is_working, :pressure, :runtime_minutes)
                   RETURNING *
                """
        with self._transaction() as conn:
            for pump in pumps:
                saved_pump = conn.execute(query, to_row(pump)).fetchone()
                saved_pumps.append(from_row(saved_pump))
        return saved_pumps

    def get_pumps_by_date(self, date: date) -> Iterable[Pump | None]:
        query = "SELECT * FROM pumps WHERE DATE(timestamp) = ?"
        with self._transaction() as conn:
            result = conn.execute(
                query,
                [
                    date.isoformat(),
                ],
            ).fetchall()
        return [from_row(row) for row in result]
