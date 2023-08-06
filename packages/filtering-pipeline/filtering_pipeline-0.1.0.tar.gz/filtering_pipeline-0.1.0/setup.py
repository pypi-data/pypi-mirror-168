# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filtering_pipeline',
 'filtering_pipeline.filters',
 'filtering_pipeline.filters.catalog_filter',
 'filtering_pipeline.filters.catalog_source',
 'filtering_pipeline.pipe',
 'filtering_pipeline.utils']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml==6.0']

setup_kwargs = {
    'name': 'filtering-pipeline',
    'version': '0.1.0',
    'description': 'This package implements the design pattern tube and filters for making AI pipeline pre- and post-processing',
    'long_description': '# Preprocessing\n\n\n\n## Installation\n\n\nWe use conda as an environment manager and poetry as dependency manager.\n\n1. Generate a conda env \nFirst, create and activate a basic conda env from the [env_prep.yml](./env/env_prep.yml) file. \n\nRun \n```\n    conda env create -f ./env/env_prep.yml\n```\n\nthen \n\n```\n    conda activate env_prep\n```\n\nNB: it can be good to change the conda name env into [env_basic_conda.yml](./env/env_basic_conda.yml) file.\n\n\n2. Install poetry and package dependencies\n\nTo install package dependencies with poetry, \n\n```\n    poetry install\n```\n\nTo update package dependencies, \n```\n    poetry update\n```\n\n\n## Testing \n\nFor running all the tests:\n\n```\n    poetry run pytest \n```\n\nFor running a specific test: \n```\n    poetry run pytest path/my_test\n```\n\n\nSee test coverage : [TO COMPLETE]\n\n\n## Preprocessing pipeline \n\n- [How does the preprocessing pipeline works?](docs/pipeline_preprocessing/pipeline.md)\n\n\n## Good pratices \n\n### PEP8\n\nUse the pep8 norm to format all the code. Specific pep8 parameters are given into the [pyproject.toml](pyproject.toml) file.\n\n```\nautopep8 --in-place --aggressive --aggressive ./\n```\n\n\n### FLAKE8\n\n[TO COMPLETE]\n',
    'author': 'Frederique Robin',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.9,<4.0.0',
}


setup(**setup_kwargs)
