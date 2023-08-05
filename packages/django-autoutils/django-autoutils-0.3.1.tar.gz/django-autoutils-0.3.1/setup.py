# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_autoutils']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0,<5.0',
 'Markdown>=3.0,<4.0',
 'Pillow>=9.0,<10.0',
 'Pygments>=2.0,<3.0',
 'autoutils>=0.1,<0.2',
 'django-admin-autocomplete-filter>=0.7,<0.8',
 'django-admin-list-filter-dropdown>=1.0,<2.0',
 'djangorestframework>=3.0,<4.0']

setup_kwargs = {
    'name': 'django-autoutils',
    'version': '0.3.1',
    'description': 'Some Good Function In Django',
    'long_description': '# django-autoutils',
    'author': 'Reza Zeiny',
    'author_email': 'rezazeiny1998@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rezazeiny/django-autoutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
