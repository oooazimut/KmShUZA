from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Group,
    Next,
    NumberedPager,
    StubScroll,
    SwitchTo,
)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from infra.bot.states import MainSG

from .custom.babel_calendar import CustomCalendar

main_menu = Dialog(
    Window(
        Const("Введите пароль"),
        TextInput(id="passwd_input"),
        state=MainSG.passw,
    ),
    Window(
        StaticMedia(),
        Next(),
        state=MainSG.curr_info,
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
