# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wp_dt']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9,<2.0']

setup_kwargs = {
    'name': 'wp-dt',
    'version': '0.0.6',
    'description': 'WP Data type',
    'long_description': '# WP data type\n\n[![Upload Python Package To Pypi](https://github.com/QiYuTechOrg/wp_dt/actions/workflows/python-publish.yml/badge.svg)](https://github.com/QiYuTechOrg/wp_dt/actions/workflows/python-publish.yml)\n[![Code Format Check](https://github.com/QiYuTechOrg/wp_dt/actions/workflows/code-format.yml/badge.svg)](https://github.com/QiYuTechOrg/wp_dt/actions/workflows/code-format.yml)\n\nWP Data Type\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
