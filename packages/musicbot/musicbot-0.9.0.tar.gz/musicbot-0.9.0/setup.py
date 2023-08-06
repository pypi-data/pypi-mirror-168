# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musicbot', 'musicbot.cli', 'musicbot.commands']

package_data = \
{'': ['*']}

install_requires = \
['PyICU>=2.9,<3.0',
 'Pygments>=2.11.2,<3.0.0',
 'attrs>=21.4.0,<22.0.0',
 'beartype>=0.10.0,<0.11.0',
 'beets>=1.6.0,<2.0.0',
 'click-skeleton>=0.26,<0.27',
 'colorlog>=6.4.1,<7.0.0',
 'edgedb>=0.24.0,<0.25.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'humanize>=4.0.0,<5.0.0',
 'more-itertools>=8.14.0,<9.0.0',
 'mutagen>=1.44.0,<2.0.0',
 'natsort>=8.1.0,<9.0.0',
 'progressbar2>=4.0.0,<5.0.0',
 'prompt_toolkit>=3.0.2,<4.0.0',
 'pyacoustid>=1.1,<2.0',
 'pydub>=0.25.1,<0.26.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'python-slugify>=6.0.1,<7.0.0',
 'python-vlc>=3.0,<4.0',
 'requests>=2.24.0,<3.0.0',
 'rich>=12.0.0,<13.0.0',
 'spotipy>=2.16.0,<3.0.0',
 'types-PyYAML>=6.0.8,<7.0.0',
 'types-python-slugify>=6.1.0,<7.0.0',
 'types-requests>=2.25.0,<3.0.0',
 'uvloop>=0.17.0,<0.18.0',
 'watchdog>=2.0.2,<3.0.0',
 'yt-dlp>=2022.8.8,<2023.0.0']

entry_points = \
{'console_scripts': ['musicbot = musicbot.main:main']}

setup_kwargs = {
    'name': 'musicbot',
    'version': '0.9.0',
    'description': 'Music swiss army knife',
    'long_description': 'None',
    'author': 'Adrien Pensart',
    'author_email': 'crunchengine@gmail.com',
    'maintainer': 'Adrien Pensart',
    'maintainer_email': 'crunchengine@gmail.com',
    'url': 'https://github.com/AdrienPensart/musicbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
