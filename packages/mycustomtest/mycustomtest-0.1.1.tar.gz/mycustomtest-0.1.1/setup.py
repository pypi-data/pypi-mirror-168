# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mycustomtest']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['mct = mycustomtest.main:app']}

setup_kwargs = {
    'name': 'mycustomtest',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'mycustomtest',
    'author_email': 'mycustomtest@example.com',
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
