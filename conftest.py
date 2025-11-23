import pytest

from infra.repo.sqlite.pumprepo import SqlitePumpRepo
from infra.receiver.modbus.modbus_receiver import ModbusReceiver


@pytest.fixture
async def repo(tmp_path):
    db_path = tmp_path / "test_db.sqlite3"
    r = SqlitePumpRepo(db_path, "tests/test_table.sql")
    await r.connect()
    yield r
    await r.close_conn()


@pytest.fixture
async def mb_receiver():
    class Settings:
        host: str = "kitvideovpn.ru"
        port: int = 23052

    r = ModbusReceiver(Settings)
    await r._connect()
    yield r
    r.close()
