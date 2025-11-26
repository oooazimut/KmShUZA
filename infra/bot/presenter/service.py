from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

from domain.models import Pump, Uza

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"


class ImageService:
    def __init__(self) -> None:
        self._curr_info_image_path: Path = IMAGES_DIR / "curr_info.png"
        self._val_color = (0, 0, 215)
        self._active_color = (243, 243, 243)
        self._passive_color = (136, 136, 136)

    def get_curr_info_img_path(self):
        return self._curr_info_image_path

    @lru_cache(maxsize=10)
    def _get_font(self, size: int):
        return ImageFont.truetype(font=BASE_DIR / "fonts/Ubuntu-R.ttf", size=size)

    def _new_image(self):
        bg = Image.new("RGBA", (1000, 650), (213, 213, 213))
        draw = ImageDraw.Draw(bg)
        return bg, draw

    def _draw_uza(self, point: Tuple[int, int], uza: Uza, draw: ImageDraw.ImageDraw):
        x, y = point
        height, width = 130, 200
        uza_font = self._get_font(48)
        selectors_font = self._get_font(40)
        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=10,
            fill=self._active_color if uza.is_active else self._passive_color,
            outline="black",
            width=5,
        )
        draw.text((x + 40, y + 40), f"УЗА {uza.number}", font=uza_font, fill="black")
        if uza.selector:
            draw.text(
                (x + 30, y + 130),
                f"выбран\nнасос {uza.selector}",
                font=selectors_font,
                align="center",
                fill=self._val_color,
            )

    def _draw_uzas_row(self, uzas: List[Uza], draw: ImageDraw.ImageDraw):
        x, y = 30, 40
        x_step = 245
        for uza in uzas:
            self._draw_uza((x, y), uza, draw)
            x += x_step

    def _draw_pump(self, point: Tuple[int, int], pump: Pump, draw: ImageDraw.ImageDraw):
        x, y = point
        width, height = 270, 250
        title_font = self._get_font(42)
        label_font = self._get_font(38)
        val_font = self._get_font(40)

        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=10,
            fill=self._active_color if pump.is_working else self._passive_color,
            outline="black",
            width=5,
        )
        draw.text((x + 50, y + 30), f"НАСОС {pump.name}", font=title_font, fill="black")
        draw.text(
            (x + 30, y + 100),
            f"{pump.pressure}",
            fill=self._val_color,
            font=val_font,
        )
        draw.text(
            (x + 30, y + 160),
            f"{pump.runtime}",
            fill=self._val_color,
            font=val_font,
        )
        draw.text((x + 140, y + 100), "бар", fill="black", font=label_font)
        draw.text((x + 140, y + 160), "час.", fill="black", font=label_font)

    def _draw_pumps_row(self, pumps: List[Pump], draw: ImageDraw.ImageDraw):
        x, y = 30, 330
        x_step = 330
        for pump in pumps:
            self._draw_pump((x, y), pump, draw)
            x += x_step

    def present_curr_info(self, uzas: List[Uza], pumps: List[Pump]):
        bg, draw = self._new_image()

        self._draw_uzas_row(uzas, draw)
        self._draw_pumps_row(pumps, draw)
        bg.save(self._curr_info_image_path)

    def present_archive_info(self, data: list[Pump]):
        pass
