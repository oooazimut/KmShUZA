from aiogram_dialog import Dialog, Window

from infra.bot.states import MainSG


main_menu = Dialog(
    Window(state=MainSG.passw),
    Window(state=MainSG.main),
    Window(state=MainSG.curr_info),
    Window(state=MainSG.calendar),
    Window(state=MainSG.archive),
)
