from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    passw = State()
    curr_info = State()
    calendar = State()
    archive = State()
