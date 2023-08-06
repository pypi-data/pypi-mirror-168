# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markline']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'furl>=2.1.3,<3.0.0',
 'pandoc>=2.2,<3.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'markline',
    'version': '0.1.0',
    'description': 'Convert Markup to Markdown with a transformation pipeline.',
    'long_description': 'None',
    'author': 'Hugh Cameron',
    'author_email': 'hescameron+githubprojects@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
