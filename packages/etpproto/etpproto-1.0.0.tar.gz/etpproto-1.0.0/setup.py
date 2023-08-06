# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etpproto', 'etpproto.protocols']

package_data = \
{'': ['*']}

install_requires = \
['coverage[toml]>=6.2,<7.0', 'etptypes>=1.0.0,<2.0.0', 'fastavro==1.5.3']

setup_kwargs = {
    'name': 'etpproto',
    'version': '1.0.0',
    'description': 'ETP protocol implementation',
    'long_description': 'ETP Protocol Implementation\n==========\n\n[![License](https://img.shields.io/pypi/l/etpproto)](https://github.com/geosiris-technologies/etpproto-python/blob/main/LICENSE)\n[![Documentation Status](https://readthedocs.org/projects/etpproto-python/badge/?version=latest)](https://etpproto-python.readthedocs.io/en/latest/?badge=latest)\n[![Python CI](https://github.com/geosiris-technologies/etpproto-python/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/geosiris-technologies/etpproto-python/actions/workflows/ci-tests.yml)\n![Python version](https://img.shields.io/pypi/pyversions/etpproto-python)\n[![PyPI](https://img.shields.io/pypi/v/etpproto-python)](https://badge.fury.io/py/etpproto-python)\n![Status](https://img.shields.io/pypi/status/etpproto-python)\n[![codecov](https://codecov.io/gh/geosiris-technologies/etpproto-python/branch/main/graph/badge.svg)](https://codecov.io/gh/geosiris-technologies/etpproto-python)\n\n\n\n\nInstallation\n----------\n\nEtpproto-python can be installed with pip : \n\n```console\npip install etpproto\n```\n\nor with poetry: \n```console\npoetry add etpproto\n```\n\n\nDeveloping\n----------\n\nFirst clone the repo from gitlab.\n\n```console\n    git clone https://github.com/geosiris-technologies/etpproto-python.git\n```\n\nTo develop, you should use **[Poetry](https://python-poetry.org/)**.\n\nInstall all necessary packages (including for development) with:\n\n```console\n    poetry install\n```\n\nThen setup the Git pre-commit hook for **[Black](<https://github.com/psf/black>)** and **[Pylint](https://www.pylint.org/)**  by running\n\n```console\n    poetry run pre-commit install\n```\n\nas the ``rev`` gets updated through time to track changes of different hooks,\nsimply run\n\n```console\n    poetry run pre-commit autoupdate\n```\nto have pre-commit install the new version.\n\nTo bump a new version of the project simply run: \n```console\n    poetry version [patch, minor, major]\n```\nYou must choose between the semver rules [patch, minor, major]',
    'author': 'Lionel Untereiner',
    'author_email': 'lionel.untereiner@geosiris.com',
    'maintainer': 'Lionel Untereiner',
    'maintainer_email': 'lionel.untereiner@geosiris.com',
    'url': 'http://www.geosiris.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
