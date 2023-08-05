# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['detection_datasets',
 'detection_datasets.readers',
 'detection_datasets.utils',
 'detection_datasets.writers']

package_data = \
{'': ['*']}

install_requires = \
['datasets[vision]>=2.4.0,<3.0.0',
 'joblib>=1.1.0,<2.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'detection-datasets',
    'version': '0.2.0',
    'description': 'Easily convert datasets between different formats for object detection',
    'long_description': '# detection-datasets\n',
    'author': 'Jerome Blin',
    'author_email': 'blinjrm@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/blinjrm/detection-dataset',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
