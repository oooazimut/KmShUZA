import logging
from domain.use_cases import UseCases
from infra.logger import OnceLogger

logger = logging.getLogger(__name__)


once_logger = OnceLogger()


@once_logger.log_exceptions_for_once
async def receive_and_save(use_cases: UseCases):
    data = await use_cases.receive_data()
    if data:
        await use_cases.save_received(data["pumps"])
