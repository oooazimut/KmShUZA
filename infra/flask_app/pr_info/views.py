from pathlib import Path
from flask import Blueprint, current_app
from flask.views import MethodView
from domain.use_cases import UseCases
from infra.presenter import ImageService

IMG_PATH = Path(__name__).resolve().parent / "images"
presenter = ImageService(curr_info_path=IMG_PATH)
use_cases: UseCases = current_app.config["use_cases"]


info_bp = Blueprint("info", __name__)


class CurrInfoView(MethodView):

    def get(self):
        data = use_cases.get_cache()
        presenter.present_curr_info(data["uzas"], data["pumps"])


info_bp.add_url_rule("/curr_info", view_func=CurrInfoView.as_view("curr_info"))
