# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beam', 'beam.scripts', 'beam.templates', 'beam.tests']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.18.0,<4.0.0', 'mypy>=0.971,<0.972', 'packaging>=21.3,<22.0']

setup_kwargs = {
    'name': 'beam-sdk',
    'version': '0.1.7',
    'description': '',
    'long_description': 'None',
    'author': 'luke lombardi',
    'author_email': 'luke@slai.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
