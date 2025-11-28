import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import OutdatedIntent, UnknownIntent
from redis.asyncio import Redis

from config import settings
from domain.use_cases import UseCases
from infra.bot.handlers import ui_error_handler
from infra.bot.middlewares import UseCasesMiddleWare

from .custom.media_storage import MediaIdStorage
from .dialogs import main_dialog, start_router

logger = logging.getLogger(__name__)


class BotService:
    def __init__(self) -> None:
        self._bot = Bot(
            settings.bot_token.get_secret_value(),
            default=DefaultBotProperties(parse_mode="HTML"),
        )
        self._redis = Redis(max_connections=20)
        self._dp = Dispatcher(
            storage=RedisStorage(
                self._redis,
                key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
            )
        )

    def configure(self, use_cases: UseCases):
        self._dp.include_routers(start_router, main_dialog)
        setup_dialogs(self._dp, media_id_storage=MediaIdStorage())
        self._dp.update.outer_middleware(UseCasesMiddleWare(use_cases))
        self._dp.errors.register(
            ui_error_handler, ExceptionTypeFilter(UnknownIntent, OutdatedIntent)
        )

    async def run(self):
        await self._bot.delete_webhook(drop_pending_updates=True)
        await self._dp.start_polling(self._bot)

    async def stop(self):
        await self._dp.stop_polling()
        await self._redis.aclose()
        await self._bot.session.close()
