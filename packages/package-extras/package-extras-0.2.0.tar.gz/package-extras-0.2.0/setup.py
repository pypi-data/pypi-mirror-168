# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package_extras']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'package-extras',
    'version': '0.2.0',
    'description': 'Dummy package to mark extras installation',
    'long_description': '## extras\n\nFor the detailed explanation read [this blog post]().\n\n### Usage\n\n```toml\n```\n\nAdd this or similar block to your code\n\n```python\n```\n\n### Development\n\n```bash\n$ poetry install\n$ poetry build\n\n$ poetry config pypi-token.pypi my-token\n$ poetry publish\n```',
    'author': 'Misha Behersky',
    'author_email': 'bmwant@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
