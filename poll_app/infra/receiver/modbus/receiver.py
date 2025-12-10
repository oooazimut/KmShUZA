import asyncio
import functools
import json
import logging
from typing import Any, Dict, List, Protocol

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException
from redis.asyncio import Redis

from poll_app.domain.entities import Pump, Uza
from poll_app.domain.ports import Receiver
from .mapping import convert_to_domain_models

logging.getLogger("pymodbus").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


def cache_to_redis(key: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis = Redis()
            try:
                result = await func(*args, **kwargs)
                payload = {k: [item.as_dict() for item in result[k]] for k in result}
                await redis.set(key, json.dumps(payload))
                return result
            except (ModbusException, ConnectionError):
                await redis.delete(key)

        return wrapper

    return decorator


class ModbusClientProtocol(Protocol):
    connected: bool

    async def connect(self): ...
    async def close(self): ...
    async def read_holding_registers(self, address, count): ...
    def convert_from_registers(self, words, data_type, word_order): ...


class ModbusReceiver(Receiver):
    def __init__(self, settings, client: ModbusClientProtocol | None = None):
        self._host = settings.host
        self._port = settings.port
        self._address = settings.address
        self._count = settings.count
        self._client = client or AsyncModbusTcpClient(host=self._host, port=self._port)
        self._lock = asyncio.Lock()

    async def _connect(self):
        if self._client.connected:
            return
        await self._client.connect()
        if not self._client.connected:
            raise ConnectionError("Cannot connect to Modbus Device")

    async def _reconnect(self):
        try:
            self._client.close()
        except Exception:
            pass
        self._client = AsyncModbusTcpClient(host=self._host, port=self._port)
        await self._client.connect()
        if not self._client.connected:
            raise ConnectionError("Reconnection failed")

    async def _ensure_connection(self):
        if not self._client.connected:
            await self._reconnect()

    def close(self):
        self._client.close()

    @property
    def is_connecting(self):
        return self._client.connected

    def _convert_to_float(self, words: List[int]) -> List[Any]:
        return [
            self._client.convert_from_registers(
                words[i : i + 2],
                data_type=self._client.DATATYPE.FLOAT32,
                word_order="little",
            )
            for i in range(0, len(words), 2)
        ]

    @cache_to_redis("modbus:latest")
    async def receive(self) -> Dict[str, List[Pump | Uza | None]]:
        async with self._lock:
            await self._ensure_connection()
            try:
                responce = await self._client.read_holding_registers(
                    address=self._address, count=self._count
                )
                if responce.isError():
                    raise ModbusException(responce)

                return convert_to_domain_models(
                    responce.registers, self._convert_to_float
                )

            except ModbusException as e:
                logger.error(e)
                await self._reconnect()
                raise
