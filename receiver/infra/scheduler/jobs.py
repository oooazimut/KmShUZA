import logging

from logger import OnceLogger
from receiver.domain.use_cases import UseCases

logger = logging.getLogger(__name__)


once_logger = OnceLogger()


# @once_logger.log_exceptions_for_once
async def receive_and_save(use_cases: UseCases):
    data = await use_cases.receive_data()
    if data:
        print(data)
        # await use_cases.save_received(data["pumps"])
