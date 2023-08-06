# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_cloud_configuration', 'pydantic_cloud_configuration.aws']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[dotenv]>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['pydantic-cloud-configuration = '
                     'pydantic_cloud_configuration.__main__:main']}

setup_kwargs = {
    'name': 'pydantic-cloud-configuration',
    'version': '0.0.2',
    'description': 'Pydantic Cloud Settings',
    'long_description': "# Pydantic Cloud Configuration\n\n[![PyPI](https://img.shields.io/pypi/v/pydantic-cloud-configuration.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/pydantic-cloud-configuration.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/pydantic-cloud-configuration)][python version]\n[![License](https://img.shields.io/pypi/l/pydantic-cloud-configuration)][license]\n\n[![Read the documentation at https://pydantic-cloud-configuration.readthedocs.io/](https://img.shields.io/readthedocs/pydantic-cloud-configuration/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/nilsdebruin/pydantic-cloud-configuration/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/nilsdebruin/pydantic-cloud-configuration/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/pydantic-cloud-configuration/\n[status]: https://pypi.org/project/pydantic-cloud-configuration/\n[python version]: https://pypi.org/project/pydantic-cloud-configuration\n[license]: https://opensource.org/licenses/MIT\n[read the docs]: https://pydantic-cloud-configuration.readthedocs.io/\n[tests]: https://github.com/nilsdebruin/pydantic-cloud-configuration/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/nilsdebruin/pydantic-cloud-configuration\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\nPydantic Cloud Configuration simplifies the retrieval of settings from the AWS cloud based on conventions.\n\n## Requirements\n\nPython 3.6+ required.\n\n## Installation\n\nYou can install _Pydantic Cloud Configuration_ via [pip] from [PyPI]:\n\n```console\n$ pip install pydantic-cloud-configuration\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license],\n_Pydantic Cloud Settings_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[mit license]: https://opensource.org/licenses/MIT\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/nilsdebruin/pydantic-cloud-configuration/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[contributor guide]: https://github.com/nilsdebruin/pydantic-cloud-configuration/blob/main/CONTRIBUTING.md\n[command-line reference]: https://pydantic-cloud-configuration.readthedocs.io/en/latest/usage.html\n",
    'author': 'Nils de Bruin',
    'author_email': 'nils@debruinmail.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nilsdebruin/pydantic-cloud-configuration',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
