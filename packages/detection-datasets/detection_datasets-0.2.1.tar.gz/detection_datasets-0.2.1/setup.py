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
    'version': '0.2.1',
    'description': 'Easily convert datasets between different formats for object detection',
    'long_description': '<div align="center">\n\n<img src="images/dd_logo.png" alt="logo" width="100"/>\n\n<br>\n\n# Detection datasets\n\n<a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/-Python 3.8-blue?style=flat-square&logo=python&logoColor=white"></a>\n<a href="https://black.readthedocs.io/en/stable/"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-black.svg?style=flat-square&labelColor=gray"></a>\n<a href="https://github.com/blinjrm/detection-datasets/actions/workflows/ci.yaml"><img src="https://img.shields.io/github/workflow/status/blinjrm/detection-datasets/CI?label=CI&style=flat-square"/></a>\n<a href="https://github.com/blinjrm/detection-datasets/actions/workflows/pypi.yaml"><img src="https://img.shields.io/github/workflow/status/blinjrm/detection-datasets/Python%20package?label=Build&style=flat-square"/></a>\n<a href="https://pypi.org/project/detection-datasets/"><img src="https://img.shields.io/pypi/status/detection-datasets?style=flat-square"/></a>\n\n<br>\n\n*Easily load and transform datasets for object detection.*\n\n</div>\n<br>\n\n---\n\n**Documentation**: https://blinjrm.github.io/detection-datasets/\n\n**Source Code**: https://github.com/blinjrm/detection-datasets\n\n**Datasets on Hugging Face Hub**: https://huggingface.co/detection-datasets\n\n---\n\n<br>\n\n`detection_datasets` aims to make it easier to work with detection datasets.\nThe main features are:\n* **Read** the dataset :\n    * from disk if it has already been downloaded.\n    * directly from the Hugging Face Hub if it [already exist](https://huggingface.co/detection-datasets).\n* **Transform** the dataset:\n    * Select a subset of data.\n    * Remap categories.\n    * Create new train-val-test splits.\n* **Visualize** the annotations.\n* **write** the dataset:\n    * to disk, selecting the target detection format: `COCO`, `YOLO` and more to come.\n    * to the Hugging Face Hub for easy reuse in a different environment and share with the community.\n\n## Requirements\n\nPython 3.8+\n\n`detection_datasets` is upon the great work of:\n\n* <a href="https://pandas.pydata.org/" class="external-link" target="_blank">Pandas</a> for manipulating data.\n* <a href="https://huggingface.co/" class="external-link" target="_blank">Hugging Face</a> to store and load datasets from the Hub.\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install detection_datasets\n```\n\n# Examples\n\n```Python\nfrom detection_datasets import DetectionDataset\n```\n\n## 1. Read\n\nFrom local files:\n\n```Python\nconfig = {\n    \'dataset_format\': \'coco\',                   # the format of the dataset on disk\n    \'path\': \'path/do/data/on/disk\',             # where the dataset is located\n    \'splits\': {                                 # how to read the files\n        \'train\': (\'train.json\', \'train\'),\n        \'test\': (\'test.json\', \'test\'),\n    },\n}\n\ndd = DetectionDataset()\ndd.from_disk(**config)\n\n# note that you can use method cascading as well:\n# dd = DetectionDataset().from_disk(**config)\n```\n\nFrom the Hugging Face Hub:\n\n```Python\ndd = DetectionDataset().from_hub(name=\'fashionpedia\')\n```\nCurrently supported format for reading datasets are:\n- COCO\n- *more to come*\n\nThe list of datasets available from the Hub is given by:\n```Python\nDetectionDataset().available_in_hub\n```\n\n## 2. Transform\n\nHere we select a subset of 10.000 images and create new train-val-test splits, overwritting the splits from the original dataset:\n```Python\ndd = DetectionDataset()\\\n    .from_hub(name=\'fashionpedia\')\\\n    .select(n_images=10000)\\\n    .split(splits=[0.8, 0.1, 0.1])\n```\n\n## 3. Visualize\n\nThe `DetectionDataset` objects contains several properties to analyze your data:\n\n\n```Python\ndd.data\n# This is equivlent to calling `dd.get_data(\'image\')`, and returns a DataFrame with 1 row per image\n\ndd.get_data(\'bbox\')     # Returns a DataFrame with 1 row per annotation\n\ndd.n_images             # Number of images\n\ndd.n_bbox               # Number of annotations\n\ndd.splits               # List of split names\n\ndd.split_proportions    # DataFrame with the % of iamges in each split\n\ndd.categories           # DataFrame with the categories and thei ids\n\ndd.category_names       # List of categories\n\ndd.n_categories         # Number of categories\n\n```\n\nYou can also visualize a image with its annotations in a notebook:\n```Python\ndd.show()                   # Shows a random image from the dataset\ndd.show(image_id=42)        # Shows the select image based on image_id\n```\n\n<div align="center">\n<img src="images/show.png" alt="hub viewer" width="500"/>\n</div>\n\n## 4. Write\n\nOnce the dataset is ready, you can write it to the local filesystem in a given format:\n\n```Python\ndd.to_disk(\n    dataset_format=\'yolo\',\n    name=\'MY_DATASET_NAME\',\n    path=\'DIRECTORY_TO_WRITE_TO\',\n)\n```\n\nCurrently supported format for writing datasets are:\n- YOLO\n- MMDET\n- *more to come*\n\nThe dataset can also be easily uploaded to the Hugging Face Hub, for reuse later on or in a different environment:\n```Python\ndd.to_hub(dataset_name=\'MY_DATASET_NAME\', repo_name=\'MY_REPO_OR_ORGANISATION\')\n```\nThe dataset viewer on the Hub will work out of the box, and we encourage you to update the README in your new repo to make it easier for the comminuty to use it.\n\n<div align="center">\n<img src="images/hub.png" alt="hub viewer" width="800"/>\n</div>\n',
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
