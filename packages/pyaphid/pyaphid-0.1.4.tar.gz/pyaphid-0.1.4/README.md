# Pyaphid

[![PyPI version](https://badge.fury.io/py/pyaphid.svg)](https://badge.fury.io/py/pyaphid)
[![GitHub license](https://img.shields.io/github/license/jvllmr/pyaphid)](https://github.com/jvllmr/pyaphid/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/jvllmr/pyaphid)](https://github.com/jvllmr/pyaphid/issues)
![PyPI - Downloads](https://img.shields.io/pypi/dd/pyaphid)
![Tests](https://github.com/jvllmr/pyaphid/actions/workflows/main.yml/badge.svg)
![Codecov](https://img.shields.io/codecov/c/github/jvllmr/pyaphid?style=plastic)

# Description

Pyaphid is a static analysis tool for detecting unwanted function calls in Python code.

## Installation and usage

Installation: `pip install pyaphid`

Usage: `python -m pyaphid <files and/or directories to analyze>` or `pyaphid <files and/or directories to analyze>`

### Configuration

Forbidden function calls can be configured via the `pyproject.toml`:

```toml
[tool.pyaphid]
forbidden = [
    "print", # forbid print(...)
    "pdb.run", # forbid pdb.run(...)
    "werkzeug.debug.*" # forbid werkzeug.debug.DebuggedApplication(...), werkzeug.debug.get_machine_id(...), ...
]
```

### CLI Options

- -n / --names: `Look-up all func calls and print their identifier`

## As a pre-commit hook

```yaml
- repo: https://github.com/jvllmr/pyaphid
  rev: v0.1.4
  hooks:
    - id: pyaphid
```

## Limitations

```python
# Pyaphid cannot work with star imports
from os.path import *
dirname(".") # undetected

# Pyaphid ignores relative imports
from . import something
something() # undetected

# Pyaphid doesn't track assignments
my_print = print
my_print("Hello world") # undetected
```
