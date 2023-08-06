# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minecraft_text_components',
 'minecraft_text_components.advances',
 'minecraft_text_components.minify']

package_data = \
{'': ['*'], 'minecraft_text_components': ['resources/*']}

install_requires = \
['typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'minecraft-text-components',
    'version': '3.0.1',
    'description': "A library for manipulating Minecraft's raw JSON text components",
    'long_description': "# minecraft-text-components\n\nA Python library for manipulating Minecraft's raw JSON text components\n",
    'author': 'VanillaTweaks',
    'author_email': 'team@vanillatweaks.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VanillaTweaks/minecraft-text-components',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
