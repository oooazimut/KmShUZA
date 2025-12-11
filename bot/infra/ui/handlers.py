import logging
from datetime import date

from aiogram.types import CallbackQuery, ErrorEvent, Message
from aiogram_dialog import DialogManager, StartMode

from bot.domain.entities import TgUser
from bot.domain.use_cases import UseCases
from config import settings
from infra.presenter import ImageService

from .states import MainSG

logger = logging.getLogger(__name__)


def check_passwd(passwd: str) -> str:
    if passwd == settings.passwd.get_secret_value():
        return passwd
    raise ValueError


async def wrong_passwd(msg: Message, *args, **kwargs):
    await msg.answer("Неверный пароль!")


async def right_passwd(msg: Message, wdgt, manager: DialogManager, *args, **kwargs):
    use_cases: UseCases = manager.middleware_data["use_cases"]
    await use_cases.save_user(
        TgUser(telegram_id=msg.from_user.id, name=msg.from_user.full_name)
    )
    await manager.start(state=MainSG.curr_info, mode=StartMode.RESET_STACK)


async def on_date(event: CallbackQuery, widget, manager: DialogManager, date: date):
    await manager.find("archive_scroll").set_page(0)

    use_cases: UseCases = manager.middleware_data["use_cases"]
    presenter: ImageService = manager.dialog_data["presenter"]
    pumps = await use_cases.get_from_storage_by_date(date)
    if not pumps:
        await event.answer("нет данных за эту дату!", show_alert=True)
        return

    presenter.present_archive_info(pumps)
    await manager.next()


async def ui_error_handler(event: ErrorEvent, dialog_manager: DialogManager):
    logger.warning("Сброс ошибки")
    await dialog_manager.start(MainSG.curr_info, mode=StartMode.RESET_STACK)
