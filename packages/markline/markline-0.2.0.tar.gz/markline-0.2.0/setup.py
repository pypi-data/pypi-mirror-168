# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markline']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'furl>=2.1.3,<3.0.0',
 'httpx>=0.23.0,<0.24.0',
 'pandoc>=2.2,<3.0']

setup_kwargs = {
    'name': 'markline',
    'version': '0.2.0',
    'description': 'Convert Markup to Markdown with a transformation pipeline.',
    'long_description': '# <img src="img/markline.svg" width="200">\n\n**Markline** converts HTML to Markdown and supports transformation methods borrowed from data engineering concepts. The goal of this project is to provide a simple API that renders HTML to Markdown for note management applications such as [Logseq](https://logseq.com).\n\n\n## Getting Started\n\n### Installation\n\nMarkline is available on PyPI:\n\n```bash\npython -m pip install markline\n```\n\n#### Dependencies\n\nMarkdown rendering is performed with [Pandoc](https://pandoc.org/) so the `pandoc` command-line tool needs to be available in your environment. You may follow [the official installation instructions](https://pandoc.org/installing.html)\nwhich are OS-dependent, or if you are a [conda](https://www.google.com/search?q=conda+python) user, with the following command:\n\n```bash\nconda install -c conda-forge pandoc\n```\n\nBeautiful Soup supports the HTML parser included in Python\'s standard library, but it also supports a number of third-party Python parsers. One is the [lxml parser](http://lxml.de/) which provides a good balance between performance and accuracy. More information about the parsers can be found in the [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser).\n\n For conda users, you can install the lxml package with the following command:\n\n```bash\nconda install -c conda-forge lxml\n```\n',
    'author': 'Hugh Cameron',
    'author_email': 'hescameron+githubprojects@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hughcameron/markline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
