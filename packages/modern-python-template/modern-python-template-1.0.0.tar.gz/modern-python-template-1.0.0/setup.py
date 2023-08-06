# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modern_python_template']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'desert>=2022.9.22,<2023.0.0',
 'marshmallow>=3.18.0,<4.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['modern-python-template = '
                     'modern_python_template.console:main']}

setup_kwargs = {
    'name': 'modern-python-template',
    'version': '1.0.0',
    'description': 'The Hypermordern Python Project',
    'long_description': '# Modern Python Template\n\n[![Tests](https://github.com/vivekwisdom/modern-python-template/workflows/Tests/badge.svg)](https://github.com/vivekwisdom/modern-python-template/actions?workflow=Tests)\n\n[![codecov](https://codecov.io/gh/vivekwisdom/modern-python-template/branch/main/graph/badge.svg?token=8SEKMGYU1X)](https://codecov.io/gh/vivekwisdom/modern-python-template)\n\n[![PyPI](https://img.shields.io/pypi/v/modern-python-template.svg)](https://pypi.org/project/modern-python-template/)\n\nmodern-python-template\n',
    'author': 'Vivek Wisdom',
    'author_email': 'ervivekwisdom@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/VivekWisdom/modern-python-template',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
