from aiogram_dialog import DialogManager

from domain.use_cases import UseCases
from infra.bot.presenter import create_service

service = create_service()


async def curr_info_getter(dialog_manager: DialogManager, **kwargs):
    use_cases: UseCases = dialog_manager.middleware_data["use_cases"]
    data = await use_cases.get_cache()
    service.present_curr_info(pumps=data["pumps"], uzas=data["uzas"])

    return {"path": service.get_curr_info_img_path()}
