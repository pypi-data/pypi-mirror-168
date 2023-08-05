# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bad_enums']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bad-enums',
    'version': '1.0.0',
    'description': 'A very bad custom implementation of enums in Python.',
    'long_description': '# bad_enums\n\nThis is a custom enums implementation for Python that is probably worse than the stdlib implementation.\n\nNew features:\n\n- The ability to allow for more than one type for enum members\n- Inheriting enum members\n',
    'author': 'EmreTech',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
