# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['desktopography']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'daiquiri>=3.2.1,<4.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['desktopography = desktopography.cli:main']}

setup_kwargs = {
    'name': 'desktopography',
    'version': '1.3',
    'description': 'Desktopography command line',
    'long_description': 'Desktopography command line\n===========================\n\nsee http://www.desktopography.net\n\nUsage\n-----\n\n``` console\n$ pip install desktopography\n$ desktopography -h\n```\n\nTODO\n----\n\n- Add more verbose documentation and docstrings\n- Add tests\n- Setup CI\n- Auto-detect screen size\n- Fix XDG support\n- Add changelog\n\nDevelopment\n-----------\n\n``` console\n$ git clone https://gitlab.com/fbochu/desktopography.git\n$ cd desktopography\n$ poetry install\n```\n\nTests\n-----\n\n``` console\n$ poetry run prospector src/\n$ poetry run black src/\n$ poetry run isort src/\n$ poetry run mypy src/\n```\n\nPublishing\n----------\n\n``` console\n$ poetry version <patch|minor|major>\n$ poetry build\n$ poetry publish\n```\n',
    'author': 'Fabien Bochu',
    'author_email': 'fabien.bochu+desktopography@nenio.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/fbochu/desktopography',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
