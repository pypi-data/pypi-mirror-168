# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaito_model']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.0,<0.6.0', 'pynamodb>=5.2.1,<6.0.0']

setup_kwargs = {
    'name': 'kaito-model',
    'version': '0.1.1',
    'description': '',
    'long_description': '## How to create a python library with projen\n\n1. run `pj new python --name=kaito_model`\n2. configure `.projenrc.py` by adding below\n\n   ```python\n        license=None,\n        project_type=ProjectType.LIB,\n        pip=False,\n        venv=False,\n        setuptools=False,\n        poetry=True,\n        poetry_options={\n        "repository": "https://github.com/MetaSearch-IO/KaitoModelPython.git",\n        },\n        deps=[\n            "python@^3.9",\n        ],\n   ```\n\n   Note that python dependency is required by [poetry](https://python-poetry.org/docs/) and the version should be at least 3.7\n\n3. run `pj build` to install dependencies and generate artifacts\n\n## Bonus\n\n1. How to enforce pre commit actions (for any language)\n\n   1. install [pre-commit](https://pre-commit.com) and add pre-commit to deps list.\n   2. create a pre-commit configuration file `.pre-commit-config.yaml` similar to below\n\n      ```yaml\n      # See https://pre-commit.com for more information\n      # See https://pre-commit.com/hooks.html for more hooks\n      repos:\n        - repo: https://github.com/pre-commit/pre-commit-hooks\n          rev: v3.2.0\n          hooks:\n            - id: trailing-whitespace\n            - id: end-of-file-fixer\n              exclude: ^\\.* # Most dot files managed by projen and are read only\n            - id: check-yaml\n            - id: check-added-large-files\n      ```\n\n   3. run `pre-commit install`\n   4. (optional) run `pre-commit autoupdate` to update hooks to the latest version\n',
    'author': 'kaito-hao',
    'author_email': 'anya@kaito.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MetaSearch-IO/KaitoModelPython',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
