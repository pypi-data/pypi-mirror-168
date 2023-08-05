# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hvac',
 'hvac.api',
 'hvac.api.auth_methods',
 'hvac.api.secrets_engines',
 'hvac.api.system_backend',
 'hvac.constants',
 'hvac.v1']

package_data = \
{'': ['*']}

install_requires = \
['pyhcl>=0.4.4,<0.5.0', 'requests==2.27.1']

setup_kwargs = {
    'name': 'hvac',
    'version': '1.0.1',
    'description': 'HashiCorp Vault API client',
    'long_description': '# hvac\n\n----\n\n![Header image](https://raw.githubusercontent.com/hvac/hvac/main/docs/_static/hvac_logo_800px.png)\n\n[HashiCorp](https://hashicorp.com/) [Vault](https://www.vaultproject.io) API client for Python 3.x\n\n[![Test](https://github.com/hvac/hvac/workflows/Test/badge.svg)](https://github.com/hvac/hvac/actions?query=workflow%3ATest)\n[![codecov](https://codecov.io/gh/hvac/hvac/branch/main/graph/badge.svg)](https://codecov.io/gh/hvac/hvac)\n[![Documentation Status](https://readthedocs.org/projects/hvac/badge/)](https://hvac.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/hvac.svg)](https://badge.fury.io/py/hvac)\n[![Twitter - @python_hvac](https://img.shields.io/twitter/follow/python_hvac.svg?label=Twitter%20-%20@python_hvac&style=social?style=plastic)](https://twitter.com/python_hvac)\n[![Gitter chat](https://badges.gitter.im/hvac/community.png)](https://gitter.im/hvac/community)\n\nTested against the latest release, HEAD ref, and 3 previous minor versions (counting back from the latest release) of Vault.\nCurrent official support covers Vault v1.4.7 or later.\n\n> **_NOTE:_**  Support for EOL Python versions will be dropped at the end of 2022.  Starting in 2023, hvac will track\n> with the CPython EOL dates.\n\n## Installation\n\n```console\npip install hvac\n```\n\nIf you would like to be able to return parsed HCL data as a Python dict for methods that support it:\n\n```console\npip install "hvac[parser]"\n```\n\n## Documentation\n\nAdditional documentation for this module available at: [hvac.readthedocs.io](https://hvac.readthedocs.io/en/stable/usage/index.html):\n\n* [Getting Started](https://hvac.readthedocs.io/en/stable/overview.html#getting-started)\n* [Usage](https://hvac.readthedocs.io/en/stable/usage/index.html)\n* [Advanced Usage](https://hvac.readthedocs.io/en/stable/advanced_usage.html)\n* [Source Reference / Autodoc](https://hvac.readthedocs.io/en/stable/source/index.html)\n* [Contributing](https://hvac.readthedocs.io/en/stable/contributing.html)\n* [Changelog](https://hvac.readthedocs.io/en/stable/changelog.html)\n',
    'author': 'Ian Unruh',
    'author_email': 'ianunruh@gmail.com',
    'maintainer': 'Brian Scholer',
    'maintainer_email': None,
    'url': 'https://github.com/hvac/hvac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
