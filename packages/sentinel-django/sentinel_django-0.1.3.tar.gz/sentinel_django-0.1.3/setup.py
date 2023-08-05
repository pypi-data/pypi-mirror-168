# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentinel_django']

package_data = \
{'': ['*']}

install_requires = \
['Django==4.0.6',
 'asgiref==3.5.2',
 'certifi==2022.6.15',
 'charset-normalizer==2.1.0',
 'idna==3.3',
 'requests==2.28.1',
 'sqlparse==0.4.2',
 'tzdata==2022.1',
 'urllib3==1.26.11']

setup_kwargs = {
    'name': 'sentinel-django',
    'version': '0.1.3',
    'description': 'Error Detection Package for Sentinel',
    'long_description': 'None',
    'author': 'Niranjan',
    'author_email': 'niranjannb7777@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
