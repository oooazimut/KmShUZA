from aiogram_dialog import DialogManager

from infra.presenter import ImageService

from bot.domain.use_cases import UseCases


async def curr_info_getter(dialog_manager: DialogManager, **kwargs):
    use_cases: UseCases = dialog_manager.middleware_data["use_cases"]
    presenter: ImageService = dialog_manager.middleware_data["presenter"]
    data = await use_cases.get_cache()

    if data:
        presenter.present_curr_info(pumps=data["pumps"], uzas=data["uzas"])
        img_path = presenter.curr_info_img_path
    else:
        img_path = presenter.nodata_img_path

    return {"path": img_path}


async def archive_getter(dialog_manager: DialogManager, **kwargs):
    presenter = dialog_manager.middleware_data["presenter"]
    curr_page = await dialog_manager.find("archive_scroll").get_page()
    trends_path = presenter.trends_path

    return {
        "pages": 3,
        "path": trends_path / f"{curr_page + 1}.png",
    }
