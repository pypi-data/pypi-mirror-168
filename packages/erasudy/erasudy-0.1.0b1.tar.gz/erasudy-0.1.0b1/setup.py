# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erasudy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

entry_points = \
{'console_scripts': ['erasudy_run = erasudy.main:run']}

setup_kwargs = {
    'name': 'erasudy',
    'version': '0.1.0b1',
    'description': 'A tool for securely erasing data',
    'long_description': '# Erasudy\n\nErase disks data securely.\n\n\n## Introduction\n\nErasudy is a tool for erasing disk data securely.\n\n\n## Development\n\n### Requirements\n\nUse `poetry install` to get the virtual environments with requirements.\n\n# Create a new release\n\nUse Poetry to create a new release.\n\nTo update the version from  and   use the following plugin.\n\n```bash\npoetry self add poetry-bumpversion\n```\n\nThen create the new release with those steps.\n\n```bash\npoetry version <version>\npoetry build\npoetry publish\n```\n',
    'author': 'blkpws',
    'author_email': 'blkpws@blackpaws.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
