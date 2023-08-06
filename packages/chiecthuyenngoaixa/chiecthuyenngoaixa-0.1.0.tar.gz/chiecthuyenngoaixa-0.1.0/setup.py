# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctnx']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chiecthuyenngoaixa',
    'version': '0.1.0',
    'description': 'An utility library for processing Vietnamese texts',
    'long_description': '# vina',
    'author': 'IoeCmcomc',
    'author_email': '53734763+IoeCmcomc@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/IoeCmcomc/chiecthuyenngoaixa',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
