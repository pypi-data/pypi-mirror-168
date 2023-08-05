from collections.abc import Callable
import math
import random
import sys

from . import crawler
from . import db


def distance_from(preferred_size: str) -> Callable[[str], float]:
    def distance(size: str):
        return math.sqrt(
            sum(
                (x - y) ** 2
                for x, y in zip(_size_tuple(preferred_size), _size_tuple(size))
            )
        )

    return distance


def _size_tuple(string: str) -> tuple[int, int]:
    x, y = string.split("x")
    return int(x), int(y)


def best_size(wallpaper_url: str, preferred_size: str) -> str:
    sizes = crawler.get_wallpaper_size(wallpaper_url)
    ordered_sizes = sorted(sizes, key=distance_from(preferred_size))
    return sizes[ordered_sizes[0]]


def select_random_wallpaper(size: str | None = None) -> str:
    size = size or f"{sys.maxsize}x{sys.maxsize}"
    wallpaper = random.choice(db.get_wallpapers())
    return best_size(wallpaper, size)
