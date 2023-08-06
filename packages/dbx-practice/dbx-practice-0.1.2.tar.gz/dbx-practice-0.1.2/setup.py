# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbx_practice']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hello = dbx_practice.say_hello:hello',
                     'say_hello = dbx_practice.say_hello:say_hello']}

setup_kwargs = {
    'name': 'dbx-practice',
    'version': '0.1.2',
    'description': '',
    'long_description': '# dbx-practice\nPractice with dbx\n',
    'author': 'Peter',
    'author_email': 'petnguyen@axon.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
