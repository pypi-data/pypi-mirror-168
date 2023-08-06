# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_to_galaxy',
 'django_to_galaxy.admin',
 'django_to_galaxy.api',
 'django_to_galaxy.api.serializers',
 'django_to_galaxy.api.views',
 'django_to_galaxy.migrations',
 'django_to_galaxy.models',
 'django_to_galaxy.schemas']

package_data = \
{'': ['*'], 'django_to_galaxy': ['templates/admin/*']}

install_requires = \
['Django>=4.0.3,<5.0.0',
 'Markdown>=3.3.6,<4.0.0',
 'bioblend>=0.16.0,<0.17.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'requests-cache>=0.9.5,<0.10.0']

setup_kwargs = {
    'name': 'django-to-galaxy',
    'version': '0.3.0',
    'description': 'Django extension that eases communication with Galaxy instance to execute workflows.',
    'long_description': 'None',
    'author': 'Kenzo-Hugo Hillion',
    'author_email': 'hillion.kenzo@posteo.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
