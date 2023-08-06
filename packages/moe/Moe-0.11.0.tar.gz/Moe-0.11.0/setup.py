# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moe',
 'moe.library',
 'moe.plugins',
 'moe.plugins.add',
 'moe.plugins.duplicate',
 'moe.plugins.edit',
 'moe.plugins.moe_import',
 'moe.plugins.move',
 'moe.plugins.musicbrainz',
 'moe.plugins.remove',
 'moe.util',
 'moe.util.cli',
 'moe.util.core']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.15,<2.0.0',
 'Unidecode>=1.2.0,<2.0.0',
 'alembic>=1.4.2,<2.0.0',
 'dynaconf>=3.1.4,<4.0.0',
 'mediafile>=0.6.0,<0.7.0',
 'musicbrainzngs>=0.7.1,<0.8.0',
 'pluggy>=0.13.1,<0.14.0',
 'pyyaml>=5.3.1,<6.0.0',
 'questionary>=1.9.0,<2.0.0']

extras_require = \
{'docs': ['furo>=2021.7.5-beta.38,<2022.0.0', 'Sphinx>=4.0.2,<5.0.0']}

entry_points = \
{'console_scripts': ['moe = moe.cli:main']}

setup_kwargs = {
    'name': 'moe',
    'version': '0.11.0',
    'description': 'The ultimate tool for managing your music library.',
    'long_description': "###############\nWelcome to Moe!\n###############\nMoe is our resident Music-Organizer-Extraordinaire who's sole purpose is to give you full control over your music library. In other words, it's a commandline-interface for managing your music.\n\n*******************\nDevelopment Warning\n*******************\nMoe is currently in early development, and is still training for his goal to become your all-powerful music library assistant. I do not recommend using Moe for anything except experimentation or testing until v1.0 is released.\n\nSo what can Moe do right now?\n=============================\n* Add music to your library, fixing tags with metadata from Musicbrainz.\n* Organize, remove, list, and edit your music in the library.\n* Supports including extra files with an album e.g. log or playlist files.\n* Supports tags with multiple values.\n\nIf you want to learn more, check out the `Getting Started <https://mrmoe.readthedocs.io/en/latest/getting_started.html>`_ docs.\n",
    'author': 'Jacob Pavlock',
    'author_email': 'jtpavlock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MoeMusic/Moe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
