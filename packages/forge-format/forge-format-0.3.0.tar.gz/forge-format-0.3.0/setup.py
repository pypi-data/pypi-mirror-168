# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forgeformat', 'forgeformat.management', 'forgeformat.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.0.0',
 'click>=8.0.0',
 'forge-core>=0.4.0,<1.0.0',
 'isort>=5.0.0',
 'python-dotenv']

entry_points = \
{'console_scripts': ['forge-format = forgeformat:cli']}

setup_kwargs = {
    'name': 'forge-format',
    'version': '0.3.0',
    'description': 'Formatting library for Forge',
    'long_description': 'A unified, opinionated code formatting command for Django projects.\n\nUses [black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/) to format Python code.\n\n\n## Installation\n\n### Django + Forge Quickstart\n\nIf you use the [Forge Quickstart](https://www.forgepackages.com/docs/forge/quickstart/),\neverything you need will be ready and available as `forge format`.\n\n### Install for existing Django projects\n\nFirst, install `forge-format` from [PyPI](https://pypi.org/project/forge-format/):\n\n```sh\npip install forge-format\n```\n\nThen add it to your `INSTALLED_APPS` in `settings.py`:\n\n```python\nINSTALLED_APPS = [\n    ...\n    "forgeformat",\n]\n```\n\nNow you will have access to the `format` command:\n\n```sh\npython manage.py format\n```\n',
    'author': 'Dave Gaeddert',
    'author_email': 'dave.gaeddert@dropseed.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.forgepackages.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
