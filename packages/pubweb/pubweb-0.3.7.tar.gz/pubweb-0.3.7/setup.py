# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pubweb',
 'pubweb.auth',
 'pubweb.cli',
 'pubweb.cli.interactive',
 'pubweb.clients',
 'pubweb.helpers',
 'pubweb.models',
 'pubweb.services']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.0,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'gql[requests]>=3.4.0,<4.0.0',
 'jsonschema>=4.6.1,<5.0.0',
 'pandas>=1.5.0,<2.0.0',
 'pycognito>=2022.1.0,<2023.0.0',
 'pygithub>=1.55,<2.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'requests_aws4auth>=1.1.2,<2.0.0',
 's3fs>=2022.8.2,<2023.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['pubweb-cli = pubweb.cli.cli:main']}

setup_kwargs = {
    'name': 'pubweb',
    'version': '0.3.7',
    'description': 'CLI tool and SDK for interacting with the PubWeb platform',
    'long_description': '# PubWeb Client\n\n[![Build Python package](https://github.com/FredHutch/PubWeb-client/actions/workflows/package.yml/badge.svg)](https://github.com/FredHutch/PubWeb-client/actions/workflows/package.yml)\n[![Lint and run tests](https://github.com/FredHutch/PubWeb-client/actions/workflows/lint.yml/badge.svg)](https://github.com/FredHutch/PubWeb-client/actions/workflows/lint.yml)\n![](https://img.shields.io/pypi/v/pubweb.svg)\n\nA Python 3.8+ library for the PubWeb platform.\n\n## Installation\n\nYou can install PubWeb using pip\n\n`pip install pubweb`\n\nor by cloning the repo and running\n\n`python setup.py install`\n\n## Usage\n\n### CLI Usage\n\nRun `pubweb-cli configure` to configure your login credentials.\n\nSpecify the `--interactive` flag to gather the command arguments interactively. \n\nExample:\n\n```bash\n$ pubweb-cli upload --interactive\n? What project is this dataset associated with?  Test project\n? Enter the full path of the data directory  /shared/biodata/test\n? Please confirm that you wish to upload 20 files (0.630 GB)  Yes\n? What type of files?  Illumina Sequencing Run\n? What is the name of this dataset?  test\n? Enter a description of the dataset (optional)\n```\n\n\n#### Listing datasets:\n```bash\nUsage: pubweb-cli list_datasets [OPTIONS]\n\n  List available datasets\n\nOptions:\n  --project TEXT         ID of the project\n  --interactive          Gather arguments interactively\n  --help                 Show this message and exit.\n```\n\n\n#### Downloading a dataset:\n```bash\nUsage: pubweb-cli download [OPTIONS]\n\n  Download dataset files\n\nOptions:\n  --project TEXT         Name or ID of the project\n  --dataset TEXT         ID of the dataset\n  --data-directory TEXT  Directory to store the files\n  --interactive          Gather arguments interactively\n  --help                 Show this message and exit.\n```\n\n#### Uploading a dataset:\n```bash\nUsage: pubweb-cli upload [OPTIONS]\n\n  Upload and create a dataset\n\nOptions:\n  --name TEXT             Name of the dataset\n  --description TEXT      Description of the dataset (optional)\n  --project TEXT          Name or ID of the project\n  --process TEXT          Name or ID of the ingest process\n  --data-directory TEXT   Directory you wish to upload\n  --interactive           Gather arguments interactively\n  --use-third-party-tool  Use third party tool for upload (Generate manifest and one-time upload authentication token)\n  --help                  Show this message and exit.\n```\n\n### SDK Usage\n\n| Sample                                                               | Description                   |\n|----------------------------------------------------------------------|-------------------------------|\n| [01_Intro](samples/01_Intro.ipynb)                                   | Authenticating and installing |\n| [02_Uploading_a_dataset](samples/02_Uploading_a_dataset.ipynb)       |                               |\n| [03_Downloading_a_dataset](samples/03_Downloading_a_dataset.ipynb)   |                               |\n| [04_Interacting_with_files](samples/04_Interacting_with_files.ipynb) |                               |\n| [05_Analyzing_a_dataset](samples/05_Analyzing_a_dataset.ipynb)       |                               |\n| [06_Using_references](samples/06_Using_references.ipynb)             | Managing reference data       |\n',
    'author': 'Fred Hutch',
    'author_email': 'viz@fredhutch.org',
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
