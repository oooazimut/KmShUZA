from aiogram import Router
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Group,
    Next,
    NumberedPager,
    StubScroll,
    SwitchTo,
)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from aiogram.filters import CommandStart

from domain.use_cases import UseCases
from infra.bot.getters import archive_getter, curr_info_getter
from infra.bot.handlers import check_passwd, on_date, right_passwd, wrong_passwd
from infra.bot.states import MainSG

from .custom.babel_calendar import CustomCalendar

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
            type_factory=check_passwd,
            on_success=right_passwd,
            on_error=wrong_passwd,
        ),
        state=MainSG.passw,
    ),
    Window(
        StaticMedia(path=Format("{path}"), type=ContentType.PHOTO),
        Button(Const("Обновить"), id="refresh_curr"),
        Next(Const("Архив")),
        state=MainSG.curr_info,
        getter=curr_info_getter,
    ),
    Window(
        Const("Выберите дату"),
        CustomCalendar(id="calendar", on_click=on_date),
        Back(Const("Назад")),
        state=MainSG.calendar,
    ),
    Window(
        StaticMedia(path=Format("{path}"), type=ContentType.PHOTO),
        StubScroll(id="archive_scroll", pages="pages"),
        Group(NumberedPager(scroll="archive_scroll")),
        Back(Const("К выбору даты")),
        SwitchTo(Const("Гл.страница"), id="switch_to_main", state=MainSG.curr_info),
        state=MainSG.archive,
        getter=archive_getter,
    ),
)
