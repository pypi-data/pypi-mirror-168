# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlflow_mlserver_docker']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.76,<2.0.0',
 'mlflow-skinny>=1.28.0,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-on-whales>=0.52.0,<0.53.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['mlflow-mlserver-docker = mlflow_mlserver_docker.cli:app']}

setup_kwargs = {
    'name': 'mlflow-mlserver-docker',
    'version': '0.3.0',
    'description': 'Package mlflow models as mlserver docker images',
    'long_description': 'None',
    'author': 'Martin Morset',
    'author_email': 'mmorset@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
