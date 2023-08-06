# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywencai']

package_data = \
{'': ['*']}

install_requires = \
['PyExecJS>=1.5.1,<2.0.0', 'pandas>=1.5.0,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pywencai',
    'version': '0.1.0',
    'description': '',
    'long_description': '# pywencai\n获取同花顺问财数据\n',
    'author': 'pluto',
    'author_email': 'mayuanchi1029@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
