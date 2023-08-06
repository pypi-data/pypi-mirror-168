# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iii_tap_pendo']

package_data = \
{'': ['*'], 'iii_tap_pendo': ['schemas/*', 'schemas/shared/*']}

install_requires = \
['backoff==1.8.0',
 'ijson==3.1.4',
 'pyhumps==1.3.1',
 'requests>=2.28.1,<3.0.0',
 'singer-python==5.12.2']

setup_kwargs = {
    'name': 'iii-tap-pendo',
    'version': '0.4.3',
    'description': 'Singer.io tap for extracting data from Pendo. Forked from https://github.com/singer-io/tap-pendo',
    'long_description': 'None',
    'author': 'Everet Rummel',
    'author_email': 'everet.rummel@clarivate.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
