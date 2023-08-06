# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minecraft_text_components',
 'minecraft_text_components.advances',
 'minecraft_text_components.contrib',
 'minecraft_text_components.minify']

package_data = \
{'': ['*'], 'minecraft_text_components': ['resources/*']}

install_requires = \
['typing-extensions>=4.3.0,<5.0.0']

extras_require = \
{'beet': ['beet>=0.73.3,<0.74.0', 'mecha>=0.57.0,<0.58.0']}

setup_kwargs = {
    'name': 'minecraft-text-components',
    'version': '3.1.1',
    'description': "A library for manipulating Minecraft's raw JSON text components",
    'long_description': "# minecraft-text-components\n\nA Python library for manipulating Minecraft's raw JSON text components\n\n## minify `beet` plugin\n\nThis library comes bundled with an optional beet plugin to automatically minify all text components inside commands. To use, install the optional dependency as described below:\n\n```bash\npip install minecraft-text-components[beet]\n```\n\nThen, you can require the plugin inside your beet configuration file:\n\n```yaml\nrequire:\n    - minecraft_text_components.contrib.beet_minify\n\npipeline:\n    - mecha\n```\n",
    'author': 'VanillaTweaks',
    'author_email': 'team@vanillatweaks.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VanillaTweaks/minecraft-text-components',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
