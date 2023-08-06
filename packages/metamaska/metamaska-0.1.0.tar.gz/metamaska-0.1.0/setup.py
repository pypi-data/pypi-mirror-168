# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metamaska', 'tests']

package_data = \
{'': ['*'], 'metamaska': ['models/*']}

install_requires = \
['click==8.0.1', 'scikit-learn>=1.1.2,<2.0.0']

extras_require = \
{'dev': ['tox>=3.26.0,<4.0.0',
         'virtualenv>=20.16.5,<21.0.0',
         'pip>=22.2.2,<23.0.0',
         'twine>=4.0.1,<5.0.0',
         'pre-commit>=2.20.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.3.1,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.8.1,<4.0.0',
         'mkdocs-material>=8.5.2,<9.0.0',
         'mkdocstrings-python>=0.7.1,<0.8.0',
         'mkdocs-autorefs>=0.4.1,<0.5.0'],
 'test': ['black>=22.8.0,<23.0.0',
          'isort>=5.10.1,<6.0.0',
          'flake8>=5.0.4,<6.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.971,<0.972',
          'pytest>=7.1.3,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['metamaska = metamaska.cli:main']}

setup_kwargs = {
    'name': 'metamaska',
    'version': '0.1.0',
    'description': 'malevolent payload classifier',
    'long_description': '#  μετάμάσκα - malevolent payload classifier\nmeta.mask can detect different types of malicious payloads like SQL injection, XSS, path-traversal, and command injection payloads.\n\n[![pypi](https://img.shields.io/pypi/v/metamaska.svg)](https://pypi.org/project/metamaska/)\n[![python](https://img.shields.io/pypi/pyversions/metamaska.svg)](https://pypi.org/project/metamaska/)\n[![Build Status](https://github.com/dogancanbakir/metamaska/actions/workflows/dev.yml/badge.svg)](https://github.com/dogancanbakir/metamaska/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/dogancanbakir/metamaska/branch/main/graphs/badge.svg)](https://codecov.io/github/dogancanbakir/metamaska)\n\n\n\n* Documentation: <https://dogancanbakir.github.io/metamaska>\n* GitHub: <https://github.com/dogancanbakir/metamaska>\n* PyPI: <https://pypi.org/project/metamaska/>\n* Free software: MIT\n\n\n## TODO\n\n* support more types\n* support interoperable model formats, more at [here](https://scikit-learn.org/stable/model_persistence.html#interoperable-formats)\n\n## Credits\n\n- [Cookiecutter](https://github.com/audreyr/cookiecutter)\n- [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage)\n- [ML-based-WAF](https://github.com/vladan-stojnic/ML-based-WAF)\n- [WAF-A-MoLE](https://github.com/AvalZ/WAF-A-MoLE)\n',
    'author': 'Doğan Can Bakır',
    'author_email': 'dogancanbakir@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dogancanbakir/metamaska',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
