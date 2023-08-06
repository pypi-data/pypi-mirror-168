# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dwr']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.11.4,<0.12.0']

entry_points = \
{'console_scripts': ['dwr = dwr.cli.core:dispatcher']}

setup_kwargs = {
    'name': 'dwr',
    'version': '0.1.0',
    'description': 'An automated documentation assistant built in Python and TeX for procedural, data-driven reporting.',
    'long_description': '# dwr\n\n<p align="center">\n<a href="https://pypi.org/project/flexi" target="_blank">\n    <img src="https://img.shields.io/pypi/v/flexi?label=version&logo=python&logoColor=%23fff&color=306998" alt="PyPI - Version">\n</a>\n\n<a href="https://pypi.org/project/flexi" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/flexi.svg?logo=python&logoColor=%23fff&color=306998" alt="PyPI - Version">\n</a>\n</p>\n\nAn automated documentation assistant built in Python and TeX for procedural, data-driven reporting.\n\n## Installation\n\n`dwr` is available through PyPI:\n\n```bash\n  pip install dwr\n```\n',
    'author': 'Elliott Phillips',
    'author_email': 'elliott.phillips.dev@gmail.com',
    'maintainer': 'Elliott Phillips',
    'maintainer_email': 'elliott.phillips.dev@gmail.com',
    'url': 'https://github.com/ellsphillips/dwr',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
