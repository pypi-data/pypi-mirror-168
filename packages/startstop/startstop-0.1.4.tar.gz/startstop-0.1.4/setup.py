# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['startstop']
entry_points = \
{'console_scripts': ['startstop = startstop:main']}

setup_kwargs = {
    'name': 'startstop',
    'version': '0.1.4',
    'description': 'Tiny process manager for Linux, MacOS and Unix-like systems',
    'long_description': None,
    'author': 'Yuri Escalianti',
    'author_email': 'yuriescl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yuriescl/startstop',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
