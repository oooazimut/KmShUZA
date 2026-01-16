from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

from domain.entities import Pump, Uza

from .tools import group_pumps_by_name

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
TRENDS_DIR = IMAGES_DIR / "trends"


class Colors:
    ACTIVE = "#f3f3f3"
    PASSIVE = "#A8A8A8"
    VALUE = "#0000d7"
    BG = "#d5d5d5"


@lru_cache(maxsize=10)
def get_font(size: int):
    return ImageFont.truetype(font=BASE_DIR / "fonts/Ubuntu-R.ttf", size=size)


class ImageService:
    def __init__(self, curr_info_path: Path = IMAGES_DIR / "curr_info.png") -> None:
        self._uza_drawer = UzaDrawer()
        self._pump_drawer = PumpDrawer()
        self._pump_plotter = PumpPlotter()
        self._curr_info_image_path: Path = curr_info_path
        self._trends_path: Path = TRENDS_DIR
        self._nodata_image_path: Path = IMAGES_DIR / "nodata.png"

    @property
    def curr_info_img_path(self):
        return self._curr_info_image_path

    @property
    def nodata_img_path(self):
        return self._nodata_image_path

    @property
    def trends_path(self):
        return self._trends_path

    def _new_image(self):
        bg = Image.new("RGBA", (1000, 650), (213, 213, 213))
        draw = ImageDraw.Draw(bg)
        return bg, draw

    def present_curr_info(self, uzas: List[Uza], pumps: List[Pump]):
        bg, draw = self._new_image()
        self._uza_drawer.draw_uzas_row(uzas, draw)
        self._pump_drawer.draw_pumps_row(pumps, draw)
        bg.save(self._curr_info_image_path)

    def present_archive_info(self, data: List[Pump]):
        pumps = group_pumps_by_name(data)
        self._pump_plotter.plot_trends(pumps)


class UzaDrawer:
    def __init__(self) -> None:
        self._uza_font = get_font(42)
        self._selectors_font = get_font(40)

    def _draw_uza(self, point: Tuple[int, int], uza: Uza, draw: ImageDraw.ImageDraw):
        x, y = point
        height, width = 130, 200
        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=10,
            fill=Colors.ACTIVE if uza.is_active else Colors.PASSIVE,
            outline="black",
            width=4,
        )
        draw.text(
            (x + 50, y + 35),
            f"УЗА {uza.number}",
            font=self._uza_font,
            fill="black",
        )
        if uza.selector:
            draw.text(
                (x + 30, y + 130),
                f"выбран\nнасос {uza.selector}",
                font=self._selectors_font,
                align="center",
                fill=Colors.VALUE,
            )

    def draw_uzas_row(self, uzas: List[Uza], draw: ImageDraw.ImageDraw):
        x, y = 30, 40
        x_step = 245
        for uza in uzas:
            self._draw_uza((x, y), uza, draw)
            x += x_step


class PumpDrawer:
    def __init__(self) -> None:
        self._title_font = get_font(42)
        self._label_font = get_font(38)
        self._value_font = get_font(40)

    def _draw_pump(self, point: Tuple[int, int], pump: Pump, draw: ImageDraw.ImageDraw):
        x, y = point
        width, height = 270, 250

        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=10,
            fill=Colors.ACTIVE if pump.is_working else Colors.PASSIVE,
            outline="black",
            width=4,
        )
        draw.text(
            (x + 60, y + 30),
            f"насос {pump.name}",
            font=self._title_font,
            fill="black",
        )
        draw.text(
            (x + 30, y + 100),
            f"{pump.pressure}",
            fill=Colors.VALUE,
            font=self._value_font,
        )
        draw.text(
            (x + 30, y + 160),
            f"{pump.runtime}",
            fill=Colors.VALUE,
            font=self._value_font,
        )
        draw.text((x + 140, y + 100), "бар", fill="black", font=self._label_font)
        draw.text((x + 140, y + 160), "час.", fill="black", font=self._label_font)

    def draw_pumps_row(self, pumps: List[Pump], draw: ImageDraw.ImageDraw):
        x, y = 30, 330
        x_step = 330
        for pump in pumps:
            self._draw_pump((x, y), pump, draw)
            x += x_step


class PumpPlotter:
    def plot_trends(self, pumps: Dict[str, List]):
        for pump in pumps:
            self._plot_trend(pumps[pump])

    def _plot_trend(self, pumps: List[Pump]):
        plt.clf()
        ax = plt.gca()
        ax.set_facecolor(Colors.BG)
        times = [p.timestamp for p in pumps]
        pressures = [p.pressure for p in pumps]
        plt.scatter(times, pressures, label="давление", c=Colors.VALUE, s=2)
        date_format = mdates.DateFormatter("%H:%M")
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(date_format)
        plt.ylim(top=4)
        plt.legend()
        plt.title(f"{pumps[0].timestamp.date()} Насос: {pumps[0].name}")
        plt.tight_layout()
        plt.savefig(TRENDS_DIR / f"{pumps[0].name}.png")
        plt.close()
