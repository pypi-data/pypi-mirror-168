# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['snopy', 'snopy._elements']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.4,<2.0.0', 'snowflake-connector-python>=2.7.12,<3.0.0']

setup_kwargs = {
    'name': 'snopy',
    'version': '0.1.1',
    'description': 'Snowflake API connector for Python',
    'long_description': None,
    'author': 'Mateusz Polakowski',
    'author_email': 'mateusz.polakowski.ds@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
