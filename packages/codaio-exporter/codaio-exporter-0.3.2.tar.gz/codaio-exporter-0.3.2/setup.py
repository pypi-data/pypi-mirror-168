# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codaio_exporter', 'codaio_exporter.api', 'codaio_exporter.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiohttp>=3.8.1,<4.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'ensure>=1.0.2,<2.0.0',
 'rich>=12.4.4,<13.0.0',
 'types-aiofiles>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['codaio-exporter = codaio_exporter.__main__:main']}

setup_kwargs = {
    'name': 'codaio-exporter',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'Sebastian Messmer',
    'author_email': 'mail@smessmer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
