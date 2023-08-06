# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamicrendergrpc', 'dynamicrendergrpc.Core']

package_data = \
{'': ['*'],
 'dynamicrendergrpc': ['Static/*',
                       'Static/Cache/Emoji/*',
                       'Static/Cache/Face/*',
                       'Static/Cache/Pendant/*',
                       'Static/Font/*',
                       'Static/Picture/*']}

install_requires = \
['emoji==1.6.3',
 'fonttools>=4.33.3,<5.0.0',
 'grpcio-tools>=1.46.3,<2.0.0',
 'grpcio>=1.46.3,<2.0.0',
 'httpx>=0.23.0,<0.24.0',
 'loguru>=0.6.0,<0.7.0',
 'opencv-python-headless>=4.6.0,<5.0.0',
 'pillow>=9.1.1,<10.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'qrcode>=7.3.1,<8.0.0']

setup_kwargs = {
    'name': 'dynamicrendergrpc',
    'version': '1.0.7',
    'description': '',
    'long_description': 'None',
    'author': 'DMC',
    'author_email': 'lzxder@github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
