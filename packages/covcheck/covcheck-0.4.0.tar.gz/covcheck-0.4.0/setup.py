# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covcheck', 'covcheck._cli', 'covcheck._parsing']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['covcheck = covcheck._cli.main:run']}

setup_kwargs = {
    'name': 'covcheck',
    'version': '0.4.0',
    'description': 'Code coverage validation',
    'long_description': '# covcheck\n\nCommand-line tool for code coverage validation.\n\n`covcheck` is intended to be used in conjunction with [coverage.py](https://coverage.readthedocs.io/), which already has support for `pytest`, `unittest`, and `nosetest`. All you have to do is point `covcheck` to the `coverage.xml` file produced when running your tests.\n\n## Installation\n\n```bash\n$ pip install coverage\n$ pip install covcheck\n```\n\n## Usage\n\n### 1. Produce a `coverage.xml` file while running your tests:\n\n```bash\n# pytest\n$ coverage run --branch -m pytest ...\n$ coverage xml\n\n# unittest\n$ coverage run --branch -m unittest ...\n$ coverage xml\n\n# nosetest\n$ coverage run --branch -m nose ...\n$ coverage xml\n```\n\n### 2. Validate that line and branch coverage meet the provided thresholds:\n\n```bash\n$ covcheck coverage.xml --line 96 --branch 84\n```\n\n## Configuration\n\nArguments passed through the command-line can also be configured with a pyproject.toml file.\n\n```bash\n$ covcheck coverage.xml --config pyproject.toml\n```\n\n```toml\n# pyproject.toml\n\n[tool.covcheck]\nline = 92.0\nbranch = 79.0\n```\n',
    'author': 'Hume AI Dev',
    'author_email': 'dev@hume.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HumeAI/covcheck',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
