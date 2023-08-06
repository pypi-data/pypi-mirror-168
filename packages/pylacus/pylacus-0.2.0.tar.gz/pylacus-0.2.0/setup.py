# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylacus']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=5.1.1,<6.0.0']}

entry_points = \
{'console_scripts': ['pylacus = pylacus:main']}

setup_kwargs = {
    'name': 'pylacus',
    'version': '0.2.0',
    'description': 'Python CLI and module for lacus',
    'long_description': '# Python client and module for Lacus\n\nUse this module to interact with a [Lacus](https://github.com/ail-project/lacus) instance.\n\n## Installation\n\n```bash\npip install pylacus\n```\n\n## Usage\n\n### Command line\n\nYou can use the `lacus` command:\n\n```bash\n```\n\n### Library\n\nSee [API Reference]()\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
