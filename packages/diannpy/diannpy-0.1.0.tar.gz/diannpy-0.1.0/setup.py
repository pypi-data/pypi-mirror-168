# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diannpy']

package_data = \
{'': ['*']}

install_requires = \
['goatools>=1.2.3,<2.0.0',
 'missingpy>=0.2.0,<0.3.0',
 'pandas>=1.4.4,<2.0.0',
 'pandera>=0.12.0,<0.13.0',
 'plotnine>=0.9.0,<0.10.0',
 'redis>=4.3.3,<5.0.0',
 'requests>=2.28.0,<3.0.0',
 'rpy2>=3.5.4,<4.0.0',
 'rq>=1.10.1,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'seaborn>=0.12.0,<0.13.0',
 'sequal>=1.0.1,<2.0.0',
 'tornado>=6.1,<7.0',
 'unimod-mapper>=0.6.6,<0.7.0',
 'uniprotparser>=1.0.8,<2.0.0']

setup_kwargs = {
    'name': 'diannpy',
    'version': '0.1.0',
    'description': "a package to provide additional report from DIANN's output of proteomics experiment",
    'long_description': None,
    'author': 'Toan Phung',
    'author_email': 'toan.phungkhoiquoctoan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
