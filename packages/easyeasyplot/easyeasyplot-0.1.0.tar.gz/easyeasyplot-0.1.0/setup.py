# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyeasyplot']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.0,<4.0.0', 'numpy>=1.23.3,<2.0.0']

setup_kwargs = {
    'name': 'easyeasyplot',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'acse-dx121',
    'author_email': 'dx121@ic.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
