# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stl']

package_data = \
{'': ['*']}

install_requires = \
['metric-temporal-logic>=0.4.0,<0.5.0', 'sympy>=1.11.1,<2.0.0']

setup_kwargs = {
    'name': 'py-signal-temporal-logic',
    'version': '0.1.1',
    'description': 'Wrapper on metric-temporal-logic to implement signal temporal logic.',
    'long_description': None,
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-signal-temporal-logic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
