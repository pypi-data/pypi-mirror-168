# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['brawling', 'brawling.models']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'brawling',
    'version': '0.3.2',
    'description': 'Brawl stars API wrapper (synchronous)',
    'long_description': '# Brawling\n\nSynchronous API wrapper for Brawl Stars made by Supercell\n\n## Installation\n\n```\npip install brawling\n```\n\nTo install with caching support (for performance)\n\n```\npip install brawling[requests-cache]\n```\n\n\nThis content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: www.supercell.com/fan-content-policy.',
    'author': 'dankmeme01',
    'author_email': 'kirill.babikov28@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
