# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fcbf']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'pandas', 'scipy']

setup_kwargs = {
    'name': 'fcbf',
    'version': '0.1.0',
    'description': 'Categorical feature selection based on information theoretical considerations',
    'long_description': 'Implementation of the fast correlation-based filter (FCBF) proposed by Yu and Liu:\n\n@inproceedings{inproceedings,\nauthor = {Yu, Lei and Liu, Huan},\nyear = {2003},\nmonth = {01},\npages = {856-863},\ntitle = {Feature Selection for High-Dimensional Data: A Fast Correlation-Based Filter Solution},\nvolume = {2},\njournal = {Proceedings, Twentieth International Conference on Machine Learning}\n}\n',
    'author': 'Martin Trat',
    'author_email': 'martin.trat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m-martin-j/fcbf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
