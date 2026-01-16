from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from domain.use_cases import UseCases
from infra.presenter.service import ImageService


class UseCasesMiddleWare(BaseMiddleware):
    def __init__(self, use_cases: UseCases) -> None:
        super().__init__()
        self._use_cases = use_cases

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["use_cases"] = self._use_cases
        return await handler(event, data)


class PresenterMiddleWare(BaseMiddleware):
    def __init__(self, presenter: ImageService) -> None:
        super().__init__()
        self._presenter = presenter

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["presenter"] = self._presenter
        return await handler(event, data)
