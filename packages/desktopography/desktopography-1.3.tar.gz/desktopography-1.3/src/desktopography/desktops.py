import enum
import pathlib

from . import db
from . import selector
from . import utils


class Desktops(enum.Enum):
    gnome = enum.auto()
    cinnamon = enum.auto()


def set_cinnamon_wallpaper(path: pathlib.Path) -> None:
    utils.gsettings(
        "set",
        "org.cinnamon.desktop.background",
        "picture-uri",
        f"'file://{path}'",
    )


def set_gnome_wallpaper(path: pathlib.Path) -> None:
    color_scheme = utils.gsettings("get", "org.gnome.desktop.interface", "color-scheme")
    utils.gsettings(
        "set",
        "org.gnome.desktop.background",
        "picture-uri-dark" if color_scheme == "prefer-dark" else "picture-uri",
        f"'file://{path}'",
    )


def set_wallpaper(desktop: Desktops, size) -> pathlib.Path:
    wallpaper_setters = {
        Desktops.cinnamon: set_cinnamon_wallpaper,
        Desktops.gnome: set_gnome_wallpaper,
    }

    wallpaper_url = selector.select_random_wallpaper(size)
    wallpaper_path = db.store(wallpaper_url)

    wallpaper_setters[desktop](wallpaper_path)
    return wallpaper_path
