# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['komposer', 'komposer.core', 'komposer.types']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'envsubst>=0.1.5,<0.2.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dotenv>=0.20',
 'stringcase>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['komposer = komposer.cli:main']}

setup_kwargs = {
    'name': 'komposer',
    'version': '0.1.6',
    'description': 'Tool to convert a Docker Compose file into a Kubernetes manifest',
    'long_description': '# komposer\n\n![main build status](https://github.com/expobrain/komposer/actions/workflows/main.yml/badge.svg?branch=main)\n\nKomposer is a CLI tool to convert a Docker Compose file into a Kubernetes manifest file so that you can deploy your Docker Compose stack it into a single Kubernetes Pod.\n\n# Documentation\n\nSee the official [documentation](https://expobrain.github.io/komposer/) for details information about the CLI usage.\n\n## To-do\n\n- set ingress annotations from CLI as file\n- set ingress paths from CLI as a file\n- able to select the Ingress class name\n- able to set custom resource limits\n- add annotations to all Kubernetes items with Komposer version\n- use labels in Docker Compose file as alternative for CLI options\n',
    'author': 'Daniele Esposti',
    'author_email': 'daniele.esposti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/expobrain/komposer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
