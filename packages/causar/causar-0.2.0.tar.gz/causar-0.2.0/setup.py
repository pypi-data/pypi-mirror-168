# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['causar', 'causar.overloads', 'causar.transactions', 'causar.typings']

package_data = \
{'': ['*']}

install_requires = \
['disnake>=2.5.2,<3.0.0']

setup_kwargs = {
    'name': 'causar',
    'version': '0.2.0',
    'description': 'A high level testing framework for Disnake bots',
    'long_description': "Causar\n---\n\n### A high level testing framework for Disnake bots\n\nWritten for my needs, open source for yours.\n\n---\n\nCurrently still in extremely early development so don't expect a lot.\n\n---\n\n### Support\n\nWant realtime help? Join the discord [here](https://discord.gg/BqPNSH2jPg).\n\n---\n\n### Funding\n\nThis project is built entirely around my current personal & freelance needs, \ntherefore it only covers the areas of Disnake I wish to test. If you want\nthis package to support further areas of Disnake consider \nsponsoring me [here](https://github.com/sponsors/Skelmis)",
    'author': 'Skelmis',
    'author_email': 'ethan@koldfusion.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Skelmis/Causar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
