# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arc',
 'arc.data',
 'arc.data.shapes',
 'arc.image',
 'arc.kube',
 'arc.model',
 'arc.tune']

package_data = \
{'': ['*'], 'arc': ['ensemble/*']}

install_requires = \
['GitPython>=3.1.26,<4.0.0',
 'blobz==0.0.13',
 'cloudpickle>=2.0.0,<3.0.0',
 'dacite>=1.6.0,<2.0.0',
 'dataclasses-jsonschema>=2.15.0,<3.0.0',
 'docker-image-py>=0.1.12,<0.2.0',
 'docker>=5.0.3,<6.0.0',
 'enlighten>=1.10.2,<2.0.0',
 'genson>=1.2.2,<2.0.0',
 'hurry.filesize>=0.9,<0.10',
 'inflection>=0.5.1,<0.6.0',
 'kubernetes==24.2.0',
 'numpy>=1.22.1,<2.0.0',
 'ocifacts>=0.0.1,<0.0.2',
 'opencontainers[reggie]>=0.0.12,<0.0.13',
 'pandas>=1.3.5,<2.0.0',
 'rootpath>=0.1.1,<0.2.0',
 'schema>=0.7.5,<0.8.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'simple-parsing==0.0.20',
 'starlette>=0.20.3,<0.21.0',
 'tableschema>=1.20.2,<2.0.0',
 'tabulate>=0.8.10,<0.9.0',
 'tomli==1.2.3',
 'typeguard>=2.13.3,<3.0.0',
 'types-tabulate>=0.8.11,<0.9.0',
 'uvicorn[standard]>=0.18.2,<0.19.0',
 'websocket-client>=1.3.3,<2.0.0',
 'xdg>=5.1.1,<6.0.0']

setup_kwargs = {
    'name': 'arc-ai',
    'version': '0.0.1',
    'description': 'Economies of models',
    'long_description': None,
    'author': 'Patrick Barker',
    'author_email': 'patrickbarkerco@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.1,<3.11',
}


setup(**setup_kwargs)
