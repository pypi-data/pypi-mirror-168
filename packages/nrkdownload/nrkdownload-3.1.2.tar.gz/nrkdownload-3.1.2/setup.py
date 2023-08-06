# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nrkdownload']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'halo>=0.0.31,<0.0.32',
 'loguru>=0.6.0,<0.7.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['nrkdownload = nrkdownload.cli:app']}

setup_kwargs = {
    'name': 'nrkdownload',
    'version': '3.1.2',
    'description': '',
    'long_description': '# nrkdownload\n\n!["Latest version"](https://img.shields.io/github/v/release/marhoy/nrk-download?include_prereleases)\n\n!["Supported Python versions"](https://img.shields.io/pypi/pyversions/nrkdownload)\n\nThis is a commandline tool to download programs and series from NRK (Norwegian public\nbroadcaster). It supports both TV, Radio and Podcast content. The tool is written in\nPython, and is compatible with Python 3.8 or newer. It has been tested under Linux, Mac\nOS X and Windows.\n\n# Documentation\n\nThe documentation for nrkdownload is availabe here: https://nrkdownload.readthedocs.org\n\n# Setting up a development environment\n\nInstall [poetry](https://python-poetry.org/), and a recent Python version (>=3.7). If\nyou want to run tests with multiple Python versions, install\n[pyenv](https://github.com/pyenv/pyenv). Set up the development environment:\n\n```bash\npoetry install\n```\n\n# Making a new release\n\n- Make sure all tests are ok by running `tox`\n- Make a pull requst on GitHub\n- Use the "new release" functionallity of GitHub. Make a new tag.\n- Update `pyproject.toml` to match the new version number.\n- `poetry build`\n- `poetry publish`\n',
    'author': 'Martin Høy',
    'author_email': 'marhoy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
