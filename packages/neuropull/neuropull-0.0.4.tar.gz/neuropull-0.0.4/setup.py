# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neuropull', 'tests']

package_data = \
{'': ['*']}

extras_require = \
{':extra == "doc"': ['mkdocs>=1.3.1,<2.0.0'],
 'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.15.2,<0.16.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'neuropull',
    'version': '0.0.4',
    'description': 'A lightweight tool for pulling connectome networks and metadata.',
    'long_description': '# neuropull\n\n\n[![pypi](https://img.shields.io/pypi/v/neuropull.svg)](https://pypi.org/project/neuropull/)\n[![python](https://img.shields.io/pypi/pyversions/neuropull.svg)](https://pypi.org/project/neuropull/)\n[![Build Status](https://github.com/neurodata/neuropull/actions/workflows/dev.yml/badge.svg)](https://github.com/neurodata/neuropull/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/neurodata/neuropull/branch/main/graphs/badge.svg)](https://codecov.io/github/neurodata/neuropull)\n\n\n\nA lightweight tool for pulling connectome networks and metadata\n\n\n* Documentation: <https://neurodata.github.io/neuropull>\n* GitHub: <https://github.com/neurodata/neuropull>\n* PyPI: <https://pypi.org/project/neuropull/>\n* Free software: MIT\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Benjamin D. Pedigo',
    'author_email': 'bpedigo@jhu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/neurodata/neuropull',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
