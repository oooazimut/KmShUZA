from aiogram_dialog import DialogManager

from domain.use_cases import UseCases
from infra.bot.presenter.service import IMAGES_DIR


async def curr_info_getter(dialog_manager: DialogManager, **kwargs):
    use_cases: UseCases = dialog_manager.middleware_data["use_cases"]
    data = await use_cases.get_cache()
    await use_cases.draw_curr_info_image(data)
    return {"path": IMAGES_DIR / settings.images.curr_info}
