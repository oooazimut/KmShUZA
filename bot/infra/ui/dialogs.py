from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets import kbd
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from . import handlers as h
from custom.babel_calendar import CustomCalendar
from domain.use_cases import UseCases
from .getters import archive_getter, curr_info_getter
from .states import MainSG

start_router = Router()


@start_router.message(CommandStart())
async def starter(msg: Message, dialog_manager: DialogManager):
    use_cases: UseCases = dialog_manager.middleware_data["use_cases"]
    user = await use_cases.get_user(msg.from_user.id)
    await dialog_manager.start(
        state=MainSG.curr_info if user else MainSG.passw,
        mode=StartMode.RESET_STACK,
    )


main_dialog = Dialog(
    Window(
        Const("Введите пароль"),
        TextInput(
            id="passwd_input",
            type_factory=h.check_passwd,
            on_success=h.right_passwd,
            on_error=h.wrong_passwd,
        ),
        state=MainSG.passw,
    ),
    Window(
        StaticMedia(path=Format("{path}"), type=ContentType.PHOTO),
        kbd.Button(Const("Обновить"), id="refresh_curr"),
        kbd.Next(Const("Архив")),
        state=MainSG.curr_info,
        getter=curr_info_getter,
    ),
    Window(
        Const("Выберите дату"),
        CustomCalendar(id="calendar", on_click=h.on_date),
        kbd.Back(Const("Назад")),
        state=MainSG.calendar,
    ),
    Window(
        StaticMedia(path=Format("{path}"), type=ContentType.PHOTO),
        kbd.StubScroll(id="archive_scroll", pages="pages"),
        kbd.Group(kbd.NumberedPager(scroll="archive_scroll")),
        kbd.Back(Const("К выбору даты")),
        kbd.SwitchTo(Const("Гл.страница"), id="switch_to_main", state=MainSG.curr_info),
        state=MainSG.archive,
        getter=archive_getter,
    ),
)
