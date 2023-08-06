# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotenv_linter',
 'dotenv_linter.grammar',
 'dotenv_linter.logics',
 'dotenv_linter.violations',
 'dotenv_linter.visitors',
 'dotenv_linter.visitors.fst']

package_data = \
{'': ['*']}

install_requires = \
['attrs',
 'click>=6,<9',
 'click_default_group>=1.2,<2.0',
 'ply>=3.11,<4.0',
 'typing_extensions>=3.6,<5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['dotenv-linter = dotenv_linter.cli:cli']}

setup_kwargs = {
    'name': 'dotenv-linter',
    'version': '0.4.0',
    'description': 'Linting dotenv files like a charm!',
    'long_description': '# dotenv-linter\n\n[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake-services.github.io)\n[![Build Status](https://github.com/wemake-services/dotenv-linter/workflows/test/badge.svg?branch=master&event=push)](https://github.com/wemake-services/dotenv-linter/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/wemake-services/dotenv-linter/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake-services/dotenv-linter)\n[![Github Action](https://github.com/wemake-services/dotenv-linter/workflows/dotenv/badge.svg)](https://github.com/wemake-services/dotenv-linter/actions?query=workflow%3Adotenv)\n[![Python Version](https://img.shields.io/pypi/pyversions/dotenv-linter.svg)](https://pypi.org/project/dotenv-linter/)\n[![Documentation Status](https://readthedocs.org/projects/dotenv-linter/badge/?version=latest)](https://dotenv-linter.readthedocs.io/en/latest/?badge=latest)\n\n---\n\nSimple linter for `.env` files.\n\n![dotenv-logo](https://raw.githubusercontent.com/wemake-services/dotenv-linter/master/docs/_static/dotenv-logo@2.png)\n\nWhile `.env` files are very simple it is required to keep them consistent.\nThis tool offers a wide range of consistency rules and best practices.\n\nAnd it integrates perfectly to any existing workflow.\n\nRead [the announcing post](https://sobolevn.me/2019/01/announcing-dotenv-linter).\n\n\n## Installation and usage\n\n```bash\npip install dotenv-linter\n```\n\nAnd then run it:\n\n```bash\ndotenv-linter .env .env.template\n```\n\nSee [Usage](https://dotenv-linter.readthedocs.io/en/latest/#usage)\nsection for more information.\n\n\n## Examples\n\nThere are many things that can go wrong in your `.env` files:\n\n```ini\n# Next line has leading space which will be removed:\n SPACED=\n\n# Equal signs should not be spaced:\nKEY = VALUE\n\n# Quotes won\'t be preserved after parsing, do not use them:\nSECRET="my value"\n\n# Beware of duplicate keys!\nSECRET=Already defined ;(\n\n# Respect the convention, use `UPPER_CASE`:\nkebab-case-name=1\nsnake_case_name=2\n```\n\nAnd much more! You can find the [full list of violations in our docs](https://dotenv-linter.readthedocs.io/en/latest/pages/violations/).\n\n\n## Pre-commit hooks\n\n`dotenv-linter` can also be used as a [pre-commit](https://github.com/pre-commit/pre-commit) hook.\nTo do so, add the following to the `.pre-commit-config.yaml` file at the root of your project:\n\n```yaml\nrepos:\n  - repo: https://github.com/wemake-services/dotenv-linter\n    rev: 0.2.0  # Use the ref you want to point at\n    hooks:\n      - id: dotenv-linter\n```\n\nFor the more detailed instructions on the pre-commit tool itself,\nplease refer to [its website](https://pre-commit.com/).\n\n## Gratis\n\nSpecial thanks goes to [Ignacio Toledo](https://ign.uy)\nfor creating an awesome logo for the project.\n',
    'author': 'sobolevn',
    'author_email': 'mail@sobolevn.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://dotenv-linter.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
