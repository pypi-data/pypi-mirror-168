# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_custom_greeter']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['my-custom-greeter = my-custom-greeter.main:app']}

setup_kwargs = {
    'name': 'my-custom-greeter',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'mateusz-lisowski',
    'author_email': 'mateusz.lisowski.dev@gmail.com',
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
