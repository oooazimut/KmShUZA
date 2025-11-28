import logging
from pathlib import Path
import aiosqlite
from config import settings

logger = logging.getLogger(__file__)


async def create_conn() -> aiosqlite.Connection:
    conn = await aiosqlite.connect(settings.db_path)
    conn.row_factory = aiosqlite.Row
    return conn


async def init_db(conn: aiosqlite.Connection):
    script_path: Path = Path(__file__).resolve().parent / "table.sql"
    logger.info(f"создаем таблицы в бд из скрипта {script_path}, если их нет...")
    with open(script_path, "r", encoding="utf-8") as file:
        await conn.executescript(file.read())
        await conn.commit()
