# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morgan']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0', 'pkginfo>=1.8.3,<2.0.0']

entry_points = \
{'console_scripts': ['morgan = morgan:main']}

setup_kwargs = {
    'name': 'morgan',
    'version': '0.10.0',
    'description': 'PyPI Mirror for Offline Environments',
    'long_description': None,
    'author': 'Ido Perlmuter',
    'author_email': 'ido@ido50.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
