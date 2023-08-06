# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pikpakapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pikpakapi',
    'version': '0.0.7',
    'description': 'PikPakAPI',
    'long_description': '# PikPakApi\n\nPikPak API Python 实现\n\n# Install\n\npip3 install pikpakapi',
    'author': 'Quan666',
    'author_email': 'i@Rori.eMail',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Quan666/PikPakAPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
