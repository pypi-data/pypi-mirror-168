# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_custom_greeter']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['mcg = my-custom-greeter.main:app']}

setup_kwargs = {
    'name': 'my-custom-greeter',
    'version': '0.1.4',
    'description': '',
    'long_description': '',
    'author': 'sindbad_the_sailor',
    'author_email': 'sindbad_the_sailor@example.com',
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
