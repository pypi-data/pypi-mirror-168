## How to create a python library with projen

1. run `pj new python --name=kaito_model`
2. configure `.projenrc.py` by adding below

   ```python
        license=None,
        project_type=ProjectType.LIB,
        pip=False,
        venv=False,
        setuptools=False,
        poetry=True,
        poetry_options={
        "repository": "https://github.com/MetaSearch-IO/KaitoModelPython.git",
        },
        deps=[
            "python@^3.9",
        ],
   ```

   Note that python dependency is required by [poetry](https://python-poetry.org/docs/) and the version should be at least 3.7

3. run `pj build` to install dependencies and generate artifacts

## Bonus

1. How to enforce pre commit actions (for any language)

   1. install [pre-commit](https://pre-commit.com) and add pre-commit to deps list.
   2. create a pre-commit configuration file `.pre-commit-config.yaml` similar to below

      ```yaml
      # See https://pre-commit.com for more information
      # See https://pre-commit.com/hooks.html for more hooks
      repos:
        - repo: https://github.com/pre-commit/pre-commit-hooks
          rev: v3.2.0
          hooks:
            - id: trailing-whitespace
            - id: end-of-file-fixer
              exclude: ^\.* # Most dot files managed by projen and are read only
            - id: check-yaml
            - id: check-added-large-files
      ```

   3. run `pre-commit install`
   4. (optional) run `pre-commit autoupdate` to update hooks to the latest version
