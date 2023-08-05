import logging
import pathlib
import re

from bs4 import BeautifulSoup
import requests

DESKTOPOGRAPHY_URL = "http://desktopography.net"
logger = logging.getLogger(__name__)


def _soup(url: str) -> BeautifulSoup:
    response = requests.get(url, timeout=10)
    return BeautifulSoup(response.text, "html.parser")


def _href(url: str, **kwargs) -> list[str]:
    return sorted(
        set(
            a.attrs["href"]
            for a in _soup(url).find_all("a", **kwargs)
            if "href" in a.attrs
        )
    )


def get_exhibitions() -> list[str]:
    logger.info("Get exhibitions from %s", DESKTOPOGRAPHY_URL)
    return _href(DESKTOPOGRAPHY_URL, href=re.compile(r"exhibition"))


def get_exhibition_wallpapers(exhibition_url: str) -> list[str]:
    logger.info("Get wallpapers from %s", exhibition_url)
    return _href(exhibition_url, href=re.compile(r"portfolios"))


def get_wallpaper_size(wallpaper_url: str) -> dict[str, str]:
    logger.info("Get available size for %s", wallpaper_url)
    return {
        a.text: a.attrs["href"]
        for a in _soup(wallpaper_url).find_all("a", class_="wallpaper-button")
        if "href" in a.attrs
    }


def store(url: str, path: pathlib.Path) -> None:
    response = requests.get(url, timeout=10)
    path.write_bytes(response.content)
