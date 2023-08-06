# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cytoplots', 'cytoplots.transforms']

package_data = \
{'': ['*']}

install_requires = \
['cytotools>=0.1.1,<0.2.0',
 'seaborn>=0.11.2,<0.12.0',
 'statannotations>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'cytoplots',
    'version': '0.1.12',
    'description': 'Plotting library for cytometry data',
    'long_description': None,
    'author': 'burtonrj',
    'author_email': 'burtonrj@cardiff.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
