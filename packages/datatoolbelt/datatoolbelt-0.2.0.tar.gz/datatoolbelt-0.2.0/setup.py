# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datatoolbelt']

package_data = \
{'': ['*']}

install_requires = \
['bumbag>=3.0.0,<4.0.0', 'pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'datatoolbelt',
    'version': '0.2.0',
    'description': 'A package for data utility functions.',
    'long_description': '<h1 align="center">datatoolbelt</h1>\n\n<p align="center">\n<a href="https://pypi.org/project/datatoolbelt"><img alt="pypi" src="https://img.shields.io/pypi/v/datatoolbelt"></a>\n<a href="https://github.com/estripling/datatoolbelt/actions/workflows/release.yml"><img alt="python" src="https://img.shields.io/pypi/pyversions/datatoolbelt.svg"></a>\n<a href="https://github.com/estripling/datatoolbelt/actions/workflows/release.yml"><img alt="os" src="https://img.shields.io/badge/OS-Ubuntu%2C%20Mac%2C%20Windows-purple"></a>\n<a href="https://github.com/estripling/datatoolbelt/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/pypi/l/datatoolbelt"></a>\n</p>\n\n<p align="center">\n<a href="https://github.com/estripling/datatoolbelt/actions/workflows/ci.yml"><img alt="ci status" src="https://github.com/estripling/datatoolbelt/actions/workflows/ci.yml/badge.svg?branch=main"></a>\n<a href="https://github.com/estripling/datatoolbelt/actions/workflows/release.yml"><img alt="release" src="https://github.com/estripling/datatoolbelt/actions/workflows/release.yml/badge.svg"></a>\n<a href="https://readthedocs.org/projects/datatoolbelt/?badge=latest"><img alt="docs" src="https://readthedocs.org/projects/datatoolbelt/badge/?version=latest"></a>\n<a href="https://codecov.io/gh/estripling/datatoolbelt"><img alt="coverage" src="https://codecov.io/github/estripling/datatoolbelt/coverage.svg?branch=main"></a>\n<a href="https://pepy.tech/project/datatoolbelt"><img alt="downloads" src="https://pepy.tech/badge/datatoolbelt"></a>\n<a href="https://github.com/psf/black"><img alt="black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://pycqa.github.io/isort/"><img alt="isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1&labelColor=ef8336"></a>\n</p>\n\n## About\n\nA package for data utility functions.\n\n## Installation\n\n`datatoolbelt` is available on [PyPI](https://pypi.org/project/datatoolbelt/):\n\n```console\npip install datatoolbelt\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing?\nCheck out the [contributing guidelines](https://datatoolbelt.readthedocs.io/en/latest/contributing.html) and the [guide for developers](https://datatoolbelt.readthedocs.io/en/latest/developers.html).\nPlease note that this project is released with a [Code of Conduct](https://datatoolbelt.readthedocs.io/en/latest/conduct.html).\nBy contributing to this project, you agree to abide by its terms.\n\n## License\n\n`datatoolbelt` was created by datatoolbelt Developers.\nIt is licensed under the terms of the BSD 3-Clause license.\n',
    'author': 'datatoolbelt Developers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/estripling/datatoolbelt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
