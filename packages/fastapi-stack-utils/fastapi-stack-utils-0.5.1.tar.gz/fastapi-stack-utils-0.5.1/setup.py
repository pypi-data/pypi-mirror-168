# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_stack_utils']

package_data = \
{'': ['*']}

install_requires = \
['asgi-correlation-id==3.0.1',
 'fastapi==0.85.0',
 'gunicorn==20.1.0',
 'python-json-logger==2.0.4',
 'pytz==2022.2.1',
 'sentry-sdk==1.9.8',
 'uvicorn[standard]==0.18.3']

setup_kwargs = {
    'name': 'fastapi-stack-utils',
    'version': '0.5.1',
    'description': 'Utils to extend the FastAPI with logging and exception handlers',
    'long_description': 'None',
    'author': 'Jonas Krüger Svensson',
    'author_email': 'jonas-ks@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
