# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxbot', 'maxbot.channels', 'maxbot.extensions', 'maxbot.flows']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'SQLAlchemy>=1.4.36,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'dateparser>=1.1.1,<2.0.0',
 'marshmallow>=3.15.0,<4.0.0',
 'number-parser>=0.2.1,<0.3.0',
 'spacy>=3.2.4,<4.0.0',
 'textdistance>=4.2.2,<5.0.0']

extras_require = \
{'all': ['python-telegram-bot[ujson]>=13.14,<14.0',
         'Flask>=2.1.2,<3.0.0',
         'python-dotenv>=0.20.0,<0.21.0'],
 'dotenv': ['python-dotenv>=0.20.0,<0.21.0'],
 'flask': ['Flask>=2.1.2,<3.0.0'],
 'telegram': ['python-telegram-bot[ujson]>=13.14,<14.0']}

entry_points = \
{'console_scripts': ['maxbot = maxbot.cli:main']}

setup_kwargs = {
    'name': 'maxbot',
    'version': '0.1.0.dev20220922223232',
    'description': '',
    'long_description': 'None',
    'author': 'Stanislav Arsentyev',
    'author_email': 'arstas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
