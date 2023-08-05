# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['safely']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'safely',
    'version': '0.2.0',
    'description': 'Capture side effects, safely.',
    'long_description': '<h1 align="center">Safely</h1>\n<p align="center">Capture side effects, safely ⚔️</p>\n<p align="center">\n<a href="https://github.com/lukemiloszewski/safely/actions/workflows/ci.yml/badge.svg" target="_blank">\n    <img src="https://github.com/lukemiloszewski/safely/actions/workflows/ci.yml/badge.svg" alt="Continuous Integration">\n</a>\n<a href="https://pypi.org/project/safely" target="_blank">\n    <img src="https://img.shields.io/pypi/v/safely?color=%2334D058&label=pypi%20package" alt="Package Version">\n</a>\n<a href="https://pypi.org/project/safely" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/safely.svg?color=%2334D058" alt="Supported Python Versions">\n</a>\n</p>\n\n## Installation\n\n```shell\npip install safely\n```\n\n## Usage\n\nAs a function (without second-order arguments):\n\n```python\ndef f(...): ...\n\nresult = safely(f)(...)\n```\n\nAs a function (with second-order arguments):\n\n```python\ndef f(...): ...\n\nresult = safely(f, logger=logger.error, message="{exc_type}: {exc_value}")(...)\n```\n\nAs a decorator (without second-order arguments):\n\n```python\n@safely\ndef f(...): ...\n\nresult = f(...)\n```\n\nAs a decorator (with second-order arguments):\n\n```python\n@safely(logger=logger.error, message="{exc_type}: {exc_value}")\ndef f(...): ...\n\nresult = f(...)\n```\n',
    'author': 'Luke Miloszewski',
    'author_email': 'lukemiloszewski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lukemiloszewski/safely',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<3.11.0',
}


setup(**setup_kwargs)
