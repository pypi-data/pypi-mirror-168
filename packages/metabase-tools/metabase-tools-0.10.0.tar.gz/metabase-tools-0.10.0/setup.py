# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metabase_tools', 'metabase_tools.endpoints', 'metabase_tools.models']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0',
 'pydantic>=1.9.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'types-requests>=2.28.9,<3.0.0']

setup_kwargs = {
    'name': 'metabase-tools',
    'version': '0.10.0',
    'description': 'Unofficial API wrapper for Metabase plus additional helper tools',
    'long_description': '# metabase-tools for python\n\nUnofficial API wrapper for Metabase plus additional helper tools\n\n[Docs](https://j01101111sh.github.io/metabase-tools/)',
    'author': 'Josh Odell',
    'author_email': 'j01101111sh@gmail.com',
    'maintainer': 'Josh Odell',
    'maintainer_email': 'j01101111sh@gmail.com',
    'url': 'https://j01101111sh.github.io/metabase-tools/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
