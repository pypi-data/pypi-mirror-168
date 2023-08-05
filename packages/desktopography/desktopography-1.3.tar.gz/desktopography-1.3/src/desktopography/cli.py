import logging

import click
import daiquiri

from . import __version__
from . import desktops
from . import selector


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    daiquiri.setup(level=logging.INFO)


@main.command()
@click.option("--size")
def shuffle(size: str | None = None):
    wallpaper = selector.select_random_wallpaper(size)
    print(wallpaper)  # noqa


@main.command()
@click.option("--size")
@click.argument("desktop", type=click.Choice([x.name for x in desktops.Desktops]))
def gsettings(desktop: str, size: str | None = None) -> None:
    wallpaper = desktops.set_wallpaper(desktops.Desktops[desktop], size)
    logging.info("Set wallpaper to %s", wallpaper)


if __name__ == "__main__":
    main()
