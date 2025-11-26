from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from domain.models import User
from domain.use_cases import UseCases
from infra.bot.states import MainSG


def check_passwd(passwd: str) -> str:
    if passwd == settings.passwd.get_secret_value():
        return passwd
    raise ValueError


async def wrong_passwd(msg: Message, *args, **kwargs):
    await msg.answer("Неверный пароль!")


async def right_passwd(msg: Message, wdgt, manager: DialogManager, *args, **kwargs):
    use_cases: UseCases = manager.middleware_data["use_cases"]
    await use_cases.save_user(User(id=msg.from_user.id, name=msg.from_user.full_name))
    await manager.start(state=MainSG.curr_info, mode=StartMode.RESET_STACK)
