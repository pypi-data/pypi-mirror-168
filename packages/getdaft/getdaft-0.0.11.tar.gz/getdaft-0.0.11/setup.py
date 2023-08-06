# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daft',
 'daft.dataframe',
 'daft.execution',
 'daft.experimental',
 'daft.experimental.datarepo',
 'daft.experimental.serving',
 'daft.experimental.serving.backends',
 'daft.experimental.serving.static',
 'daft.internal',
 'daft.logical',
 'daft.runners',
 'daft.viz']

package_data = \
{'': ['*']}

install_requires = \
['fsspec',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.16.6,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'protobuf>=3.19.0,<3.20.0',
 'pyarrow>=8.0.0,<9.0.0',
 'pydot>=1.4.2,<2.0.0',
 'ray==1.13.0',
 'tabulate>=0.8.10,<0.9.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.8.0,<4.0.0'],
 'experimental': ['fastapi>=0.79.0,<0.80.0',
                  'docker>=5.0.3,<6.0.0',
                  'uvicorn>=0.18.2,<0.19.0',
                  'cloudpickle>=2.1.0,<3.0.0',
                  'boto3>=1.23.0,<2.0.0',
                  'PyYAML>=6.0,<7.0',
                  'icebridge==0.0.3',
                  'Pillow>=9.2.0,<10.0.0'],
 'iceberg': ['icebridge==0.0.3'],
 'serving': ['fastapi>=0.79.0,<0.80.0',
             'docker>=5.0.3,<6.0.0',
             'uvicorn>=0.18.2,<0.19.0',
             'cloudpickle>=2.1.0,<3.0.0',
             'boto3>=1.23.0,<2.0.0',
             'PyYAML>=6.0,<7.0']}

entry_points = \
{'console_scripts': ['build_inplace = build:build_inplace']}

setup_kwargs = {
    'name': 'getdaft',
    'version': '0.0.11',
    'description': 'A Distributed DataFrame library for large scale complex data processing.',
    'long_description': "[![daft](https://github.com/Eventual-Inc/Daft/actions/workflows/python-package.yml/badge.svg)](https://github.com/Eventual-Inc/Daft/actions/workflows/python-package.yml)\n\n# Daft\n\n![Frame 113](https://user-images.githubusercontent.com/17691182/190476440-28f29e87-8e3b-41c4-9c28-e112e595f558.png)\n\n\n[Daft](https://www.getdaft.io) is a fast, ergonomic and scalable open-source dataframe library: built for Python and Complex Data/Machine Learning workloads.\n\n## Installation\n\nInstall Daft with `pip install getdaft`.\n\n## Documentation\n\nLearn more about Daft in our [documentation](https://docs.getdaft.io).\n\n## Community\n\nFor questions about Daft, please post in our [community hosted on GitHub Discussions](https://github.com/Eventual-Inc/Daft/discussions)! We look forward to meeting you there.\n\n## Why Daft?\n\nProcessing Complex Data such as images/audio/pointclouds often requires accelerated compute for geometric or machine learning algorithms, much of which leverages existing tooling from the Python/C++ ecosystem. However, many workloads such as analytics, model training data curation and data processing often also require relational query operations for loading/filtering/joining/aggregations.\n\nDaft marries the two worlds with a Dataframe API, enabling you to run both large analytical queries and powerful Complex Data algorithms from the same interface.\n\n1. **Python-first**: Python and Jupyter notebooks are first-class citizens. Daft handles any Python libraries and datastructures natively - use any Python library such as Numpy, OpenCV and PyTorch for Complex Data processing.\n\n2. **Laptop to Cloud**: Daft is built to run as easily on your laptop for interactive development and on your own [Ray](https://www.ray.io) cluster or [Eventual](https://www.eventualcomputing.com) deployment for terabyte-scale production workloads.\n\n3. **Open Data Formats**: Daft loads from and writes to open data formats such as Apache Parquet and Apache Iceberg. It also supports all major cloud vendors' object storage options, allowing you to easily integrate with your existing storage solutions.\n",
    'author': 'Eventual Inc',
    'author_email': 'daft@eventualcomputing.com',
    'maintainer': 'Sammy Sidhu',
    'maintainer_email': 'sammy@eventualcomputing.com',
    'url': 'https://getdaft.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
