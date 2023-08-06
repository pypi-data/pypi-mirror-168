# nmk-python
Python plugin for nmk build system

[![License: MPL](https://img.shields.io/github/license/dynod/nmk-python)](https://github.com/dynod/nmk-python/blob/main/LICENSE)
[![Checks](https://img.shields.io/github/workflow/status/dynod/nmk-python/Build/main?label=build%20%26%20u.t.)](https://github.com/dynod/nmk-python/actions?query=branch%3Amain)
[![PyPI](https://img.shields.io/pypi/v/nmk-python)](https://pypi.org/project/nmk-python/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This plugin adds support for Python development in an **`nmk`** project:
* setup file generation
* code format with [black](https://github.com/psf/black)
* import sorting with [isort](https://github.com/PyCQA/isort)
* code analysis with [flake8](https://flake8.pycqa.org/)
* python wheel build
* test with [pytest](https://pytest.org)
* VSCode settings generation (if [**`nmk-vscode`**](https://github.com/dynod/nmk-vscode) plugin is also used)

## Usage

To use this plugin in your **`nmk`** project, insert this reference:
```
refs:
    - pip://nmk-python!plugin.yml
```

## Documentation

This plugin documentation is available [here](https://github.com/dynod/nmk/wiki/nmk-python-plugin)

## Issues

Issues for this plugin shall be reported on the [main  **`nmk`** project](https://github.com/dynod/nmk/issues), using the **plugin:python** label.
