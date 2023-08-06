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
    'version': '0.4.0',
    'description': 'Package mlflow models as mlserver docker images',
    'long_description': "# Mlflow Mlserver Docker\n\nThis is a utility package for building mlserver docker images based on MLflow models on a remote\ntracking server.\n\nCurrently, the S3 backend is the only officially supported backend, but any backend should work just\nfine as long as you have all the required dependencies installed. If you're interested in other\nbackends let me know.\n\n## Installation\n\n```\npip install mlflow-mlserver-docker\n```\n\n## Usage\n\n```sh\nmlflow-mlserver-docker build runs:/fg8934ug54eg9hrdegu904/model\n```\n\n## Development\n\n```sh\npoetry install\npoetry self add poetry-version-plugin\n```\n\nMake sure `docker` is running.\n",
    'author': 'Martin Morset',
    'author_email': 'mmorset@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dingobar/mlflow-mlserver-docker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
