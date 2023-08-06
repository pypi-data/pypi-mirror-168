# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['depends']

package_data = \
{'': ['*']}

install_requires = \
['python-acache>=0,<1']

setup_kwargs = {
    'name': 'python-depends',
    'version': '0.1.0',
    'description': 'A dependency injector as in FastAPI',
    'long_description': None,
    'author': 'Dmitrij Vinokour',
    'author_email': 'dimfred.1337@web.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dimfred/depends',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
