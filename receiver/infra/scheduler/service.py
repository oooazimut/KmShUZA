from apscheduler.schedulers.asyncio import AsyncIOScheduler

from receiver.domain.use_cases import UseCases
from .jobs import receive_and_save


class SchedulerService:
    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()

    def configure(self, use_cases: UseCases):
        self._scheduler.add_job(
            receive_and_save,
            trigger="interval",
            seconds=5,
            id="receive_and_save",
            args=[use_cases],
            replace_existing=True,
        )

    def run(self):
        self._scheduler.start()

    def stop(self):
        self._scheduler.shutdown()
