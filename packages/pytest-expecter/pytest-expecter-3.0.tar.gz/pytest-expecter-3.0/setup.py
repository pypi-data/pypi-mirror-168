# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expecter']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['pytest-expecter = expecter.plugin']}

setup_kwargs = {
    'name': 'pytest-expecter',
    'version': '3.0',
    'description': 'Better testing with expecter and pytest.',
    'long_description': '# Overview\n\nA `pytest` plugin based on [garybernhardt/expecter](https://github.com/garybernhardt/expecter) to write expressive tests.\n\n[![Build Status](https://img.shields.io/travis/jacebrowning/pytest-expecter/develop.svg?label=unix)](https://travis-ci.org/jacebrowning/pytest-expecter)\n[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/pytest-expecter/develop.svg)](https://coveralls.io/r/jacebrowning/pytest-expecter)\n[![PyPI License](https://img.shields.io/pypi/l/pytest-expecter.svg)](https://pypi.org/project/pytest-expecter)\n[![PyPI Version](https://img.shields.io/pypi/v/pytest-expecter.svg)](https://pypi.org/project/pytest-expecter)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/pytest-expecter.svg?color=orange)](https://pypistats.org/packages/pytest-expecter)\n\n# Quick Start\n\nWith this plugin you can write tests (optionally using [pytest-describe](https://github.com/pytest-dev/pytest-describe)) like this:\n\n```python\ndef describe_foobar():\n\n    def it_can_pass(expect):\n        expect(2 + 3) == 5\n\n    def it_can_fail(expect):\n        expect(2 + 3) == 6\n```\n\nand get output like this:\n\n```python\n============================= FAILURES =============================\n___________________ describe_foobar.it_can_fail ____________________\n\n    def it_can_fail(expect):\n>       expect(2 + 3) == 6\nE       AssertionError: Expected 6 but got 5\n\ntest_foobar.py:7: AssertionError\n================ 1 failed, 1 passed in 2.67 seconds ================\n```\n\n# Installation\n\nInstall it directly into an activated virtual environment:\n\n```\n$ pip install pytest-expecter\n```\n\nor add it to your [Poetry](https://python-poetry.org/docs/) project:\n\n```\n$ poetry add pytest-expecter\n```\n',
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/pytest-expecter',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
