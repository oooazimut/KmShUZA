import asyncio
from typing import List, TypedDict
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from domain.models import Pump, Uza


class ModelsDict(TypedDict):
    pumps: List[Pump]
    uzas: List[Uza]


class ModbusReceiver:
    def __init__(self, settings):
        self._host = settings.host
        self._port = settings.port
        self._client = AsyncModbusTcpClient(host=self._host, port=self._port)
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
        except:
            pass
        self._client = AsyncModbusTcpClient(host=self._host, port=self._port)
        await self._client.connect()

    async def _ensure_connection(self):
        if not self._client.connected:
            await self._reconnect()

    def close(self):
        self._client.close()

    @property
    def is_connecting(self):
        return self._client.connected

    async def receive_data(self) -> ModelsDict:
        async with self._lock:
            await self._ensure_connection()
            try:
                responce = await self._client.read_holding_registers(
                    address=16384, count=16
                )
                if responce.isError():
                    raise ModbusException(responce)

                return responce.registers

            except ModbusException:
                await self._reconnect()
                raise
