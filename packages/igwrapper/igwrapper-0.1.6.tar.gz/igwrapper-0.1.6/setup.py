# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['igwrapper', 'igwrapper.clients', 'igwrapper.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[aiodns,brotli]>=3.8.1,<4.0.0',
 'lightstreamer-client-lib>=1.0.0b2,<2.0.0']

setup_kwargs = {
    'name': 'igwrapper',
    'version': '0.1.6',
    'description': '',
    'long_description': '',
    'author': 'sohaib94',
    'author_email': 'sohaib.ashraf94@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
