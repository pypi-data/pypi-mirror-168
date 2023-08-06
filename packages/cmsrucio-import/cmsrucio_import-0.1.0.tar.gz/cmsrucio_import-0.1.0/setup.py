# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmsrucio_import']

package_data = \
{'': ['*'], 'cmsrucio_import': ['templates/*']}

entry_points = \
{'console_scripts': ['cmsrucio-import = cmsrucio_import.main:app']}

setup_kwargs = {
    'name': 'cmsrucio-import',
    'version': '0.1.0',
    'description': '',
    'long_description': '# User DataManagement Tools\n\n\n## Requirements\n\n- initialise rucio (installs rucio_client) - `source /cvmfs/cms.cern.ch/rucio/setup-py3.sh`\n- initalise proxy - `voms-proxy-init -voms cms -rfc -valid 192:00`\n- export RUCIO_ACCOUNT=$USER \n\n## Additionally\npip3 install -r requirements.txt\n\n\n## How to\n\nShow list of available commands: `python3 upload.py --help`\n\nShow help related to a specific commands (cmd): `python3 upload.py <cmd> --help`\n\n<br>\n\nTo upload a local file and create a rule on it:\n- Copy template from `lib/templates/file-upload.yml`\n- Specify parameters:\n    - `filePath`: location of local file \n    - `lfn`: lfn (logical file name) for the file - `store/user/rucio/<username>/<filename>`\n    - `tempRSE`: temp RSE to use for the intermediate hop (can be left to template value)\n    - `rse`: destination RSE/RSE Expression on which rule should be created\n    - `lifetime`: life of rule\n    - `copies`: number of copies required\n\n- Execute: `python3 upload.py upload-file-yaml <yaml-file-path>`\n\n<br>\n\nTo upload a dataset create a rule on it:\n- Copy template from `lib/templates/dataset-upload.yml`\n- Specify parameters:\n    - `datasetPath`: location of folder to use as dataset \n    - `datasetName`: name of dataset conforming to CMS naming conventions\n    - `tempRSE`: temp RSE to use for the intermediate hop (can be left to template value)\n    - `rse`: destination RSE/RSE Expression on which rule should be created\n    - `lifetime`: life of rule\n    - `copies`: number of copies required\n\n- Execute: `python3 upload.py upload-dataset-yaml <yaml-file-path>`\n\n\n## Build Instructions\n\n### Prerequisite\n\nWe will be using [poetry](https://python-poetry.org/) to build the package.\n\n### Create a wheel package\n```\ncd CMSRucio/UserDMTools/cmsrucio_import\n\npoetry build\n```\n### Installing from the wheel package\n```\npip3 install --user dist/cmsrucio_import-0.1.0-py3-none-any.whl\n```\n\n\n\n\n',
    'author': 'Rahul Chauhan',
    'author_email': 'rahul.chauhan@cern.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
