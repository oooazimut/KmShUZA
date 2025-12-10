from psycopg_pool import AsyncConnectionPool
from config import settings


def create_pool() -> AsyncConnectionPool:
    dsn = (
        f"host={settings.pg.host} "
        f"port={settings.pg.port} "
        f"user={settings.pg.poller} "
        f"password={settings.pg.poller_passw.get_secret_value()} "
        f"dbname={settings.pg.db_name}"
    )

    return AsyncConnectionPool(conninfo=dsn, min_size=1, max_size=1, open=False)
