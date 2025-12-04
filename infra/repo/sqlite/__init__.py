import logging
from pathlib import Path
import sqlite3

import aiosqlite
from pumprepo import SqlitePumpRepo
from user_repo import SqliteUserRepo

from config import settings

logger = logging.getLogger(__file__)

TIMEOUT = 5


async def create_conn() -> aiosqlite.Connection:
    conn = await aiosqlite.connect(settings.db_path, timeout=3)
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def create_sync_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.db_path, timeout=3)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


async def init_db(conn: aiosqlite.Connection):
    script_path: Path = Path(__file__).resolve().parent / "table.sql"
    logger.info(f"создаем таблицы в бд из скрипта {script_path}, если их нет...")
    with open(script_path, "r", encoding="utf-8") as file:
        await conn.executescript(file.read())
        await conn.commit()
