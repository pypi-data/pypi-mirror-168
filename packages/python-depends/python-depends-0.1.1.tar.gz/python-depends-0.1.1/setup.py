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
    'version': '0.1.1',
    'description': 'A dependency injector as in FastAPI',
    'long_description': '# python-depends\n\nA dependecy injector as in (FastAPI)[https://pypi.org/project/fastapi/].\n\n## Install\n\n```\npip3 install python-depends\npip3 install git+https://github.com/Dimfred/python-depends.git\n```\n\n## Examples\n\n```python\nfrom depends import Depends, inject\n\nasync def d1():\n    # do some stuff, which takes long\n    return "some stuff"\n\nasync def d2():\n    # do some other stuff, which also takes long\n    return "some other stuff"\n\n# inject the dependency into a function\n@inject\nasync def main(d1_=Depends(d1), d2_=Depends(d2)):\n    print(d1_)  # some stuff\n    print(d2_)  # some other stuff\n```\n\nNested dependencies\n\n```python\nfrom depends import Depends, inject\n\nasync def d1():\n    # do some stuff, which takes long\n    return "some stuff"\n\nasync def d2(d1_=Depends(d1)):\n    # do some other stuff, which also takes long\n    # you can work with d2_ here\n    return "some other stuff"\n\n# d1 was called only once and is cached during the whole call\n@inject\nasync def main(d1_=Depends(d1), d2_=Depends(d2)):\n    print(d1_)  # some stuff\n    print(d2_)  # some other stuff\n```\n\nYou can also use parameters in your injected function which will be forwarded to your dependencies. The detection is done by name, no type checking is applied here.\n\n```python\nfrom depends import Depends, inject\n\nasync def d1(a):\n    return a\n\n\n# d1 was called only once and is cached during the whole call\n@inject\nasync def main(a, d1_=Depends(d1)):\n    return a, d1_\n\nassert (await main(1)) == (1, 1)\n```\n\nAnother cool thing is that you can use context managed objects inside an injected function. Like for example a database session.\n\n```python\nfrom depends import Depends, inject\n\nasync def get_db():\n    async with Session() as db:\n        yield db\n\n@inject\nasync def main(db=Depends(get_db)):\n    # do stuff with your async db connection\n    # after the exit the connection will be teared down\n```\n\n## TODO\n\n- [ ] support sync dependencies (only async rn)\n- [ ] replace the caching mechanism with maybe the correct dependency tree\n',
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
