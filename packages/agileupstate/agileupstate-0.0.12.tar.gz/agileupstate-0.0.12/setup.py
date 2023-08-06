# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['agileupstate']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.1,<9.0',
 'hvac>=1.0.2,<2.0.0',
 'prettytable>=3.3.0,<4.0.0']

entry_points = \
{'console_scripts': ['agileupstate = agileupstate.cli:cli']}

setup_kwargs = {
    'name': 'agileupstate',
    'version': '0.0.12',
    'description': 'State mangement tool for Future Agile CICD',
    'long_description': "# agileup\n\nPython 3.9+ project to assist with the management of pipeline states with the following features:\n\n* Linux and Windows compatible project.\n* Defines state model.\n* Saves and fetches model from vault.\n\n## Prerequisites\n\nThis project uses poetry is a tool for dependency management and packaging in Python. It allows you to declare the \nlibraries your project depends on, it will manage (install/update) them for you. \n\nUse the installer rather than pip [installing-with-the-official-installer](https://python-poetry.org/docs/master/#installing-with-the-official-installer).\n\n```sh\npoetry self add poetry-bumpversion\n```\n\n```sh\npoetry -V\nPoetry (version 1.2.0)\n```\n\n## Getting Started\n\n```sh\npoetry update\n```\n\n```sh\npoetry install\n```\n\n## Development\n\nThis project uses the [hvac](https://github.com/hvac/hvac) python module and to develop locally you can run vault\nas a docker service as detailed here [local docker vault](https://hub.docker.com/_/vault).\n\nUsing a random GUID for the root token of our in memory docker, e.g. `8d02106e-b1cd-4fa5-911b-5b4e669ad07a`.\n\n```sh\ndocker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=8d02106e-b1cd-4fa5-911b-5b4e669ad07a' -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' -p8200:8200 vault\n```\nCheck your connection with the following, note in development mode vault should not be sealed.\n\n```sh\nexport VAULT_ADDR='http://localhost:8200'\nexport VAULT_TOKEN='8d02106e-b1cd-4fa5-911b-5b4e669ad07a'\n\npoetry run agileupstate check\n```\n\n## Run\n```sh\npoetry run agileupstate\n```\n\n## Lint\n```sh\npoetry run flake8\n```\n\n## Test\n```sh\npoetry run pytest\n```\n\n## Publish\n\n* By default we are using [PYPI packages](https://packaging.python.org/en/latest/tutorials/installing-packages/). \n* Create yourself an access token for PYPI and then follow the instructions.\n\n```sh\nexport PYPI_USERNAME=__token__ \nexport PYPI_PASSWORD=<Your API Token>\npoetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD\n```\n\n## Versioning\nWe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Agile-Solutions-GB-Ltd/agileup/tags). \n\n## Releasing\n\nWe are using [poetry-bumpversion](https://github.com/monim67/poetry-bumpversion) to manage release versions.\n\n```sh\npoetry version patch\n```\n\n## Dependency\n\nOnce the release has been created it is now available for you to use in other python projects via:\n\n```sh\npip install agileupstate\n```\n\nAnd also for poetry projects via:\n\n```sh\npoetry add agileupstate\n```\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.\n\n## License\n\nThis project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details\n\n\n\n",
    'author': 'agileturret',
    'author_email': 'Paul.Gilligan@agilesolutions.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Agile-Solutions-GB-Ltd/agileupstate',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
