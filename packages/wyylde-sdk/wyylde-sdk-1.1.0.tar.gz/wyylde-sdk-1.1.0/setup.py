# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wyylde_sdk', 'wyylde_sdk.models']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['wyylde-sdk = wyylde_sdk.__main__:main']}

setup_kwargs = {
    'name': 'wyylde-sdk',
    'version': '1.1.0',
    'description': 'Wyylde SDK',
    'long_description': "# Wyylde SDK\n\n[![PyPI](https://img.shields.io/pypi/v/wyylde-sdk.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/wyylde-sdk.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/wyylde-sdk)][pypi status]\n[![License](https://img.shields.io/pypi/l/wyylde-sdk)][license]\n\n[![Read the documentation at https://wyylde-sdk.readthedocs.io/](https://img.shields.io/readthedocs/wyylde-sdk/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/Dogeek/wyylde-sdk/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/Dogeek/wyylde-sdk/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/wyylde-sdk/\n[read the docs]: https://wyylde-sdk.readthedocs.io/\n[tests]: https://github.com/Dogeek/wyylde-sdk/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/Dogeek/wyylde-sdk\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Wyylde SDK_ via [pip] from [PyPI]:\n\n```console\n$ pip install wyylde-sdk\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Wyylde SDK_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/Dogeek/wyylde-sdk/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/Dogeek/wyylde-sdk/blob/main/LICENSE\n[contributor guide]: https://github.com/Dogeek/wyylde-sdk/blob/main/CONTRIBUTING.md\n[command-line reference]: https://wyylde-sdk.readthedocs.io/en/latest/usage.html\n",
    'author': 'Dogeek',
    'author_email': 'simon.bordeyne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dogeek/wyylde-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
