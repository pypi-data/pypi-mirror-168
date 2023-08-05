import datetime
import json
import logging
import pathlib

from . import crawler

logger = logging.getLogger(__name__)

CACHE_DIR = pathlib.Path(
    "~/.cache/desktopography"
).expanduser()  # TODO(fbochu) XDG and config
CACHE_MAX_AGE = 120  # days


def retrieve_wallpapers() -> list[str]:
    logger.info("Get all available wallpapers...")
    return sorted(
        wallpaper
        for exhibition in crawler.get_exhibitions()
        for wallpaper in crawler.get_exhibition_wallpapers(exhibition)
    )


def is_cache_valid(path: pathlib.Path) -> bool:
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=CACHE_MAX_AGE)

    try:
        last_modified_timestamp = path.stat().st_mtime
        last_modified = datetime.datetime.fromtimestamp(last_modified_timestamp)
    except FileNotFoundError:
        return False

    return (now - last_modified) < delta


def get_wallpapers() -> list[str]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    wallpaper_list = CACHE_DIR / "wallpapers.txt"

    if not is_cache_valid(wallpaper_list):
        wallpapers = sorted(
            wallpaper
            for exhibition in crawler.get_exhibitions()
            for wallpaper in crawler.get_exhibition_wallpapers(exhibition)
        )
        with open(wallpaper_list, "w", encoding="utf-8") as fp:
            json.dump(wallpapers, fp)

    with open(wallpaper_list, encoding="utf-8") as fp:
        return json.load(fp)


def store(wallpaper_url: str) -> pathlib.Path:
    filename = wallpaper_url.rsplit("/")[-1]
    file_path = CACHE_DIR / filename

    crawler.store(wallpaper_url, file_path)

    return file_path
