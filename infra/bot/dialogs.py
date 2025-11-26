from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
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

from infra.bot.getters import curr_info_getter
from infra.bot.handlers import check_passwd, right_passwd, wrong_passwd
from infra.bot.states import MainSG

from .custom.babel_calendar import CustomCalendar

main_menu = Dialog(
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
        CustomCalendar(id="calendar"),
        Back(Const("Назад")),
        state=MainSG.calendar,
    ),
    Window(
        StaticMedia(),
        StubScroll(id="archive_scroll", pages="pages"),
        Group(NumberedPager(scroll="archive_scroll")),
        Back(Const("К выбору даты")),
        SwitchTo(Const("Гл.страница"), id="switch_to_main", state=MainSG.curr_info),
        state=MainSG.archive,
    ),
)
