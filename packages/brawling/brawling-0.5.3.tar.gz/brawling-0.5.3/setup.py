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

extras_require = \
{'cache': ['requests-cache>=0.9.6,<0.10.0']}

setup_kwargs = {
    'name': 'brawling',
    'version': '0.5.3',
    'description': 'Brawl stars API wrapper (synchronous)',
    'long_description': '# Brawling\n\nSynchronous API wrapper for Brawl Stars made by Supercell\n\n## Installation\n\n```\npip install brawling\n```\n\nTo install with caching support (for performance, optional)\n\n```\npip install brawling[cache]\n```\n\n## Usage\n\nUsage is very simple and straightforward:\n\n```py\nimport brawling\n\n# This can be either the API token,\n# or the path to the file with it.\nTOKEN = "..."\n\n# Initialize the client\nclient = brawling.Client(TOKEN)\n\nbattle_log = client.get_battle_log("#yourtag")\n\n# Prints "Battle(battle_time=...)"\nprint(battle_log[0])\n```\n\nFor some endpoints, there\'s also a possibility to page over them:\n\n```py\n# Returns a generator which fetches up to 45 total pages\n# of Ukrainian rankings for Shelly, each page\n# being a list of BrawlerRanking model where 0 < len(page) <= 10\npages = client.page_brawler_rankings(\n    brawling.BrawlerID.SHELLY,\n    per_page=10, region=\'ua\', max=450\n)\n\n# ^ Note that this operation was immediate,\n# as no data is fetched yet.\n\n# This will now fetch pages of 10 players,\n# until either there are no players left,\n# or we reach the max limit of 450.\nfor page in pages:\n    print(page)\n```\n\nIf you don\'t want to handle exceptions, want to use a dynamic IP address, or force disable caching, there are three additional options in the Client constructor:\n\n```py\nclient = Client(TOKEN, proxy=True, strict_errors=False, force_no_cache=True)\n```\n\nWith `strict_errors` set to False, the API methods can now silently fail instead of raising exceptions, and instead return an `ErrorResponse` object. It\'s your job to handle it.\n\nThe `proxy` argument will use a [3rd party proxy](https://docs.royaleapi.com/#/proxy). Details on setting up are on the linked page. DISCLAIMER: I am not responsible for anything related to the proxy. I am not in any way related to its developers, and it\'s not my fault if your API access gets blocked because of using it.\n\n`force_no_cache` will disable the caching of requests no matter what. This setting is useless if you didn\'t install with `brawling[cache]`, and otherwise is only recommended if you\'re facing issues because of the cache (such as non-up-to-date responses)\n\n## Disclaimer\n\nThis content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: www.supercell.com/fan-content-policy.',
    'author': 'dankmeme01',
    'author_email': 'kirill.babikov28@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
