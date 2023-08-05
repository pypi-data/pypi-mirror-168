# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databutton_logger']

package_data = \
{'': ['*']}

install_requires = \
['asgi-correlation-id>=3.0.1,<4.0.0',
 'fastapi>=0.80',
 'loguru>=0.6.0,<0.7.0',
 'opentelemetry-api>=1.12.0',
 'opentelemetry-exporter-zipkin>=1.12.0,<2.0.0',
 'opentelemetry-instrumentation-fastapi',
 'opentelemetry-sdk>=1.12.0']

setup_kwargs = {
    'name': 'databutton-logger',
    'version': '0.7.0',
    'description': 'Logger utilities for databutton',
    'long_description': 'None',
    'author': 'Databutton',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
