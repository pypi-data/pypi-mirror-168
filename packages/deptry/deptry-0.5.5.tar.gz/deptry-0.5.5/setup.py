# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deptry', 'deptry.dependency_getter', 'deptry.issue_finders']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=5.0.0,<6.0.0',
 'click>=8.0.0,<9.0.0',
 'isort>=5.10.1,<6.0.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{':python_full_version <= "3.7.0"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['deptry = deptry.cli:deptry']}

setup_kwargs = {
    'name': 'deptry',
    'version': '0.5.5',
    'description': 'A command line utility to check for obsolete, missing and transitive dependencies in a Python project.',
    'long_description': '<p align="center">\n  <img width="460" height="300" src="https://raw.githubusercontent.com/fpgmaas/deptry/main/docs/docs/static/deptry_Logo-01.svg">\n</p>\n\n---\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/deptry)](https://img.shields.io/github/v/release/fpgmaas/deptry)\n[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/deptry/merge-to-main)](https://img.shields.io/github/workflow/status/fpgmaas/deptry/merge-to-main)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/deptry)](https://pypi.org/project/deptry/)\n[![codecov](https://codecov.io/gh/fpgmaas/deptry/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/deptry)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/deptry)](https://img.shields.io/pypi/dm/deptry?style=flat-square)\n[![License](https://img.shields.io/github/license/fpgmaas/deptry)](https://img.shields.io/github/license/fpgmaas/deptry)\n\n_deptry_ is a command line tool to check for issues with dependencies in a Python project, such as obsolete or missing dependencies. It supports the following types of projects:\n\n- Projects that use [Poetry](https://python-poetry.org/) and a corresponding _pyproject.toml_ file\n- Projects that use a _requirements.txt_ file according to the [pip](https://pip.pypa.io/en/stable/user_guide/) standards\n\nDependency issues are detected by scanning for imported modules within all Python files in a directory and its subdirectories, and comparing those to the dependencies listed in the project\'s requirements.\n\n---\n<p align="center">\n  <a href = "https://fpgmaas.github.io/deptry">Link to the documentation</a>\n</p>\n\n---\n\n## Quickstart\n\n### Installation\n\n_deptry_ can be added to your project with \n\n```shell\npoetry add --group dev deptry\n```\n\nor with \n\n```\n<activate virtual environment>\npip install deptry\n```\n\n> **Warning**\n> When using pip to install _deptry_, make sure you install it within the virtual environment of your project. Installing _deptry_ globally will not work, since it needs to have access to the metadata of the packages in the virtual environment.\n\n### Prerequisites\n\n_deptry_ should be run withing the root directory of the project to be scanned, and the project should be running in its own dedicated virtual environment.\n\n### Usage\n\nTo scan your project for dependency issues, run\n\n```sh\ndeptry .\n```\n\n_deptry_ can be configured by using additional command line arguments, or \nby adding a `[tool.deptry]` section in _pyproject.toml_.\n\nFor more information, see the [documentation](https://fpgmaas.github.io/deptry/).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'Florian Maas',
    'author_email': 'fpgmaas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fpgmaas/deptry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
