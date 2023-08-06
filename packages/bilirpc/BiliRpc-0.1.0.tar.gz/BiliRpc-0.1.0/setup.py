# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bilirpc',
 'bilirpc.bilibili',
 'bilirpc.bilibili.ad',
 'bilirpc.bilibili.ad.v1',
 'bilirpc.bilibili.app',
 'bilirpc.bilibili.app.archive',
 'bilirpc.bilibili.app.archive.middleware',
 'bilirpc.bilibili.app.archive.middleware.v1',
 'bilirpc.bilibili.app.dynamic',
 'bilirpc.bilibili.app.dynamic.v2',
 'bilirpc.bilibili.live.app.room.v1',
 'bilirpc.bilibili.metadata',
 'bilirpc.bilibili.metadata.device',
 'bilirpc.bilibili.metadata.locale',
 'bilirpc.bilibili.metadata.network',
 'bilirpc.bilibili.rpc']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.49.1,<2.0.0']

setup_kwargs = {
    'name': 'bilirpc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'DMC',
    'author_email': 'lzxder@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
