# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reporter', 'reporter.objects']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'securityreporter',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Alexander Krigsman',
    'author_email': 'alexander.krigsman@dongit.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
