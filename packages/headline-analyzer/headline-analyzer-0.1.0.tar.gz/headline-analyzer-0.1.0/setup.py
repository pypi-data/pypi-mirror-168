# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['headline_analyzer',
 'headline_analyzer.goodheadlines',
 'headline_analyzer.inference',
 'headline_analyzer.stats',
 'headline_analyzer.utils',
 'headline_analyzer.wordbank']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'headline-analyzer',
    'version': '0.1.0',
    'description': 'Analyze headlines for optimising conversion rate',
    'long_description': None,
    'author': 'Nivrith',
    'author_email': 'nivrith.mandayam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
