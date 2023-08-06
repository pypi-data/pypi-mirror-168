# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['thymed']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1', 'rich>=12.5.1,<13.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['punch = thymed.__main__:punch_default',
                     'thymed = thymed.__main__:main']}

setup_kwargs = {
    'name': 'thymed',
    'version': '0.1.0',
    'description': 'Thymed',
    'long_description': "# Thymed\n\n[![PyPI](https://img.shields.io/pypi/v/thymed.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/thymed.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/thymed)][pypi status]\n[![License](https://img.shields.io/pypi/l/thymed)][license]\n\n[![Read the documentation at https://thymed.readthedocs.io/](https://img.shields.io/readthedocs/thymed/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/czarified/thymed/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/czarified/thymed/branch/master/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/thymed/\n[read the docs]: https://thymed.readthedocs.io/\n[tests]: https://github.com/czarified/thymed/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/czarified/thymed\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Thymed_ via [pip] from [PyPI]:\n\n```console\n$ pip install thymed\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Thymed_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/czarified/thymed/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/czarified/thymed/blob/main/LICENSE\n[contributor guide]: https://github.com/czarified/thymed/blob/main/CONTRIBUTING.md\n[command-line reference]: https://thymed.readthedocs.io/en/latest/usage.html\n",
    'author': 'Benjamin Crews',
    'author_email': 'aceF22@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/czarified/thymed',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
