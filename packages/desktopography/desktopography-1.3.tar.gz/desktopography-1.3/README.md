Desktopography command line
===========================

see http://www.desktopography.net

Usage
-----

``` console
$ pip install desktopography
$ desktopography -h
```

TODO
----

- Add more verbose documentation and docstrings
- Add tests
- Setup CI
- Auto-detect screen size
- Fix XDG support
- Add changelog

Development
-----------

``` console
$ git clone https://gitlab.com/fbochu/desktopography.git
$ cd desktopography
$ poetry install
```

Tests
-----

``` console
$ poetry run prospector src/
$ poetry run black src/
$ poetry run isort src/
$ poetry run mypy src/
```

Publishing
----------

``` console
$ poetry version <patch|minor|major>
$ poetry build
$ poetry publish
```
