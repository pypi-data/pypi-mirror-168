# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaphid']

package_data = \
{'': ['*']}

install_requires = \
['tomli>=2.0.1,<3.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pyaphid = pyaphid.cli:run']}

setup_kwargs = {
    'name': 'pyaphid',
    'version': '0.1.4',
    'description': 'Identify unwanted function calls in your code',
    'long_description': '# Pyaphid\n\n[![PyPI version](https://badge.fury.io/py/pyaphid.svg)](https://badge.fury.io/py/pyaphid)\n[![GitHub license](https://img.shields.io/github/license/jvllmr/pyaphid)](https://github.com/jvllmr/pyaphid/blob/master/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/jvllmr/pyaphid)](https://github.com/jvllmr/pyaphid/issues)\n![PyPI - Downloads](https://img.shields.io/pypi/dd/pyaphid)\n![Tests](https://github.com/jvllmr/pyaphid/actions/workflows/main.yml/badge.svg)\n![Codecov](https://img.shields.io/codecov/c/github/jvllmr/pyaphid?style=plastic)\n\n# Description\n\nPyaphid is a static analysis tool for detecting unwanted function calls in Python code.\n\n## Installation and usage\n\nInstallation: `pip install pyaphid`\n\nUsage: `python -m pyaphid <files and/or directories to analyze>` or `pyaphid <files and/or directories to analyze>`\n\n### Configuration\n\nForbidden function calls can be configured via the `pyproject.toml`:\n\n```toml\n[tool.pyaphid]\nforbidden = [\n    "print", # forbid print(...)\n    "pdb.run", # forbid pdb.run(...)\n    "werkzeug.debug.*" # forbid werkzeug.debug.DebuggedApplication(...), werkzeug.debug.get_machine_id(...), ...\n]\n```\n\n### CLI Options\n\n- -n / --names: `Look-up all func calls and print their identifier`\n\n## As a pre-commit hook\n\n```yaml\n- repo: https://github.com/jvllmr/pyaphid\n  rev: v0.1.4\n  hooks:\n    - id: pyaphid\n```\n\n## Limitations\n\n```python\n# Pyaphid cannot work with star imports\nfrom os.path import *\ndirname(".") # undetected\n\n# Pyaphid ignores relative imports\nfrom . import something\nsomething() # undetected\n\n# Pyaphid doesn\'t track assignments\nmy_print = print\nmy_print("Hello world") # undetected\n```\n',
    'author': 'Jan Vollmer',
    'author_email': 'jan@vllmr.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jvllmr/pyaphid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
