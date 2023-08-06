# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyanimalsay', 'pyanimalsay.app']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pyanimalsay = pyanimalsay.main:app']}

setup_kwargs = {
    'name': 'pyanimalsay',
    'version': '0.0.0.1',
    'description': '',
    'long_description': "## Welcome to the FARM\n### (FAstAPI, React, MongoDB)\n###\n###\n\n#### Cow says 'mo'\n#### Cat says 'meow'\n#### Dog says 'woof'",
    'author': 'sindbad_the_sailor',
    'author_email': 'sindbad_the_sailor@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
