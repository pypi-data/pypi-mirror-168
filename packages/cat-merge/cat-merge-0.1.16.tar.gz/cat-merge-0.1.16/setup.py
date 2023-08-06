# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cat_merge', 'cat_merge.model']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9',
 'grape>=0.1.24,<0.2.0',
 'mkdocs>=1.3.0,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scipy>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['cat-merge = cat_merge.cli:main']}

setup_kwargs = {
    'name': 'cat-merge',
    'version': '0.1.16',
    'description': '',
    'long_description': 'None',
    'author': 'Monarch Initiative',
    'author_email': 'info@monarchinitiative.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
