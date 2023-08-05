# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_quote_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'random-quote-generator-7368',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Random Quote Generator',
    'author': 'Atul Rai',
    'author_email': 'atul.a.rai98@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
