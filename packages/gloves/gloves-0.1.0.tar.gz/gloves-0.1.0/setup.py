# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gloves']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'gloves',
    'version': '0.1.0',
    'description': 'this project is a demonstration of a strategy for creating packages with Poetry, python-semantic-release and commitzen',
    'long_description': '',
    'author': 'Leonardo Pires',
    'author_email': 'leonardorifiol.p@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
