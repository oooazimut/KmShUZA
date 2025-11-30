from aiogram_dialog import DialogManager

from domain.use_cases import UseCases
from infra.bot.presenter import create_service

service = create_service()


async def curr_info_getter(dialog_manager: DialogManager, **kwargs):
    use_cases: UseCases = dialog_manager.middleware_data["use_cases"]
    data = use_cases.get_cache()
    if data:
        service.present_curr_info(pumps=data["pumps"], uzas=data["uzas"])
        img_path = service.curr_info_img_path
    else:
        img_path = service.nodata_img_path

    return {"path": img_path}


async def archive_getter(dialog_manager: DialogManager, **kwargs):
    curr_page = await dialog_manager.find("archive_scroll").get_page()
    trends_path = service.trends_path

    return {
        "pages": 3,
        "path": trends_path / f"{curr_page + 1}.png",
    }
