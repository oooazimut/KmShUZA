from typing import Dict, List
from domain.models import Pump, Uza
from domain.ports import InfoPresenter
from 


class ImageService(InfoPresenter):
    def _draw_uzas(self, uzas: List[Uza]):
        for uza in uzas:
            

    def _draw_pumps(self, pumps: List[Pump]):
        pass

    def present_curr_info(self, data: Dict[str, List]):
        uzas, pumps = data["uzas"], data["pumps"]
        bg = ImageService
        self._draw_uzas(uzas)
        self._draw_pumps(pumps)

    def present_archive_info(self, data: list[Pump]):
        return super().present_archive_info(data)
