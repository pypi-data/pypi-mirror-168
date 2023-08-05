# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['everytime']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'everytime',
    'version': '0.1.0',
    'description': 'Schedule asyncio coroutines',
    'long_description': '# every - Schedule asyncio coroutines\n\n## How to use\n```python\nevery(5 * minutes)(do_something)\nevery(other * day)(do_something)\nevery(minute).starting_at(hour=12, minute=15)(do_something)\n```\n\n## Example\n```python\nimport asyncio\nfrom every import *\n\nasync def do_something():\n    print("Hello")\n\nevery(2 * seconds)(do_something)\n\nloop = asyncio.get_event_loop()\nloop.run_forever()\n```\n',
    'author': 'meipp',
    'author_email': 'meipp@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/meipp/every/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
