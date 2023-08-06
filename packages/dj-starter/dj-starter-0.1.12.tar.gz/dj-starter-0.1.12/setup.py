# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djstarter',
 'djstarter.management',
 'djstarter.management.commands',
 'djstarter.migrations',
 'djstarter.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.15,<4.0.0',
 'coverage>=6.4.4,<7.0.0',
 'django-environ>=0.9.0,<0.10.0',
 'httpx[http2]>=0.23.0,<0.24.0',
 'jsonpickle>=2.1.0,<3.0.0',
 'psycopg2-binary>=2.9.2,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'wheel>=0.36.2,<0.37.0']

setup_kwargs = {
    'name': 'dj-starter',
    'version': '0.1.12',
    'description': 'Django Project Bootstraper with Common Models and Utilities',
    'long_description': 'None',
    'author': 'Adrian',
    'author_email': 'adrian@rydeas.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adrianmeraz/dj-starter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
