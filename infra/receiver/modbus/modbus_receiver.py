import asyncio
from typing import Dict, List, Protocol, TypedDict
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from domain.models import Pump, Uza


class ModbusClientProtocol(Protocol):
    connected: bool

    async def connect(self): ...
    async def close(self): ...
    async def read_holding_registers(self, address, count): ...
    def convert_from_registers(self, words, data_type, word_order): ...


class ModbusReceiver:
    def __init__(self, settings, client: ModbusClientProtocol | None = None):
        self._host = settings.host
        self._port = settings.port
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

    def _convert_to_bin(self, src: int, quantity: int) -> List[int]:
        return [int(b) for b in f"{src:0{quantity}b}"[::-1]]

    def _convert_to_float(self, words: List[int]) -> List[Any]:
        return [
            self._client.convert_from_registers(
                words[i : i + 2], data_type=self._client.DATATYPE, word_order="little"
            )
            for i in range(0, len(words), 2)
        ]

    def _convert_to_domain_models(
        self, registers: List
    ) -> Dict[str, List[Pump | Uza | None]]:
        selectors = registers[:3] + registers[17]
        permsissions = self._convert_to_bin(registers[3], 4)
        pump_conditions = self._convert_to_bin(registers[4], 3)
        uza_conditions = self._convert_to_bin(registers[5], 4)
        pressures = self._convert_to_float(registers[8:14])
        pump_runtimes = registers[14:17]
        result = {"pumps": [], "uzas": []}

        return result

    async def receive_data(
        self, address: int, count: int
    ) -> Dict[str, List[Pump | Uza | None]]:
        async with self._lock:
            await self._ensure_connection()
            try:
                responce = await self._client.read_holding_registers(
                    address=address, count=count
                )
                if responce.isError():
                    raise ModbusException(responce)

                return self._convert_data(responce.registers)

            except ModbusException:
                await self._reconnect()
                raise
