from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from domain.use_cases import UseCases


class UseCasesMiddleWare(BaseMiddleware):
    def __init__(self, use_cases: UseCases) -> None:
        super().__init__()
        self.use_cases = use_cases

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["use_cases"] = self.use_cases
        return await handler(event, data)
