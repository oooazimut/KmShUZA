from psycopg_pool import AsyncConnectionPool
from config import settings


def create_pool(user: str, password: str) -> AsyncConnectionPool:
    dsn = (
        f"host={settings.pg.host} "
        f"port={settings.pg.port} "
        f"user={user} "
        f"password={password} "
        f"dbname={settings.pg.db_name}"
    )

    return AsyncConnectionPool(conninfo=dsn, min_size=2, max_size=10, open=False)
