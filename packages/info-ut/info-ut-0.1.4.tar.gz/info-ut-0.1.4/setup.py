# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['info_ut', 'info_ut.feed']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.0.0,<23.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'feedparser>=6.0.10,<7.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'info-ut',
    'version': '0.1.4',
    'description': 'Modul python untuk medapatkan informasi terbaru dari website Universitas Terbuka',
    'long_description': '# info-ut\n\n[![PyPi Package Version](https://img.shields.io/pypi/v/info-ut)](https://pypi.org/project/info-ut/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/info-ut)](https://pypi.org/project/info-ut/)\n[![LICENSE](https://img.shields.io/github/license/UnivTerbuka/info-ut)](https://github.com/UnivTerbuka/info-ut/blob/main/LICENSE)\n[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)\n\nModul python untuk medapatkan informasi terbaru dari website Universitas Terbuka\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UnivTerbuka/info-ut',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
