# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['c7n_tencentcloud',
 'c7n_tencentcloud.actions',
 'c7n_tencentcloud.filters',
 'c7n_tencentcloud.resources']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2022.1',
 'retrying>=1.3.3,<2.0.0',
 'tencentcloud-sdk-python>=3.0.715,<4.0.0']

setup_kwargs = {
    'name': 'c7n-tencentcloud',
    'version': '0.0.0',
    'description': 'Cloud Custodian - Tencent Cloud Provider',
    'long_description': None,
    'author': 'Tencent Cloud',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
