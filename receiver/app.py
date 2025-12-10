import asyncio
import logging

from logger import configure_logging
from config import settings

from .domain.use_cases import UseCases
from .infra.receiver.modbus import ModbusReceiver


async def main():
    configure_logging(level=logging.DEBUG)
    use_cases = UseCases(ModbusReceiver(settings.modbus))
    while True:
        await use_cases.receive_and_save()
        await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
