# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_dotenv']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.1,<2.0.0', 'python-dotenv>=0.21.0,<0.22.0']

entry_points = \
{'poetry.application.plugin': ['poethepoet = poethepoet.plugin:PoetryPlugin',
                               'poetry-dotenv = '
                               'poetry_dotenv.plugin:DotenvPlugin']}

setup_kwargs = {
    'name': 'poetry-dotenv',
    'version': '0.1.0',
    'description': 'poetry-dotenv - is the plugin that automatically loads environment variables from a dotenv file into the environment before poetry commands are run.',
    'long_description': '<p align="center">\n  <a href="https://opensource.org/licenses/MIT">\n    <img alt="license" src="https://img.shields.io/pypi/l/poetry-dotenv?logo=opensourceinitiative">\n  </a>\n  <a href="https://pypi.org/project/poetry-dotenv">\n    <img alt="python" src="https://img.shields.io/pypi/pyversions/poetry-dotenv?logo=python">\n  </a>\n  <a href="https://pypi.org/project/poetry-dotenv">`\n    <img alt="pypi" src="https://img.shields.io/pypi/v/poetry-dotenv?logo=pypi">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/releases">\n    <img alt="release" src="https://img.shields.io/github/v/release/volopivoshenko/poetry-dotenv?logo=github">\n  </a>\n  <a href="https://www.sphinx-doc.org/en/master">\n    <img alt="sphinx" src="https://img.shields.io/badge/made_with-Sphinx-1f425f.svg?logo=readthedocs">\n  </a>\n  <a href="https://numpydoc.readthedocs.io/en/latest/format.html">\n    <img alt="numpydoc" src="https://img.shields.io/badge/docstrings-numpy-1f425f.svg?logo=numpy">\n  </a>\n</p>\n\n<p align="center">\n  <a href="https://github.com/psf/black">\n    <img alt="black" src="https://img.shields.io/badge/code_style-black-black.svg?logo=windowsterminal">\n  </a>\n  <a href="https://pycqa.github.io/isort/index.html">\n    <img alt="isort" src="https://img.shields.io/badge/imports-isort-black.svg?logo=windowsterminal">\n  </a>\n  <a href="https://wemake-python-stylegui.de/en/latest/index.html">\n    <img alt="wemake" src="https://img.shields.io/badge/style-wemake-black.svg?logo=windowsterminal">\n  </a>\n  <a href="https://mypy.readthedocs.io/en/stable/index.html">\n    <img alt="mypy" src="https://img.shields.io/badge/mypy-checked-success.svg?logo=python">\n  </a>\n  <a href="https://github.com/pyupio/safety">\n    <img alt="safety" src="https://img.shields.io/badge/safety-checked-success.svg?logo=windowsterminal">\n  </a>\n  <a href="https://github.com/semantic-release/semantic-release">\n    <img alt="semantic_release" src="https://img.shields.io/badge/semantic_release-angular-e10079?logo=semantic-release">\n  </a>\n</p>\n\n<p align="center">\n  <a href="https://github.com/dependabot">\n    <img alt="dependabot" src="https://img.shields.io/badge/dependabot-enable-success?logo=Dependabot">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/actions/workflows/integration.yaml">\n    <img alt="integration" src="https://img.shields.io/github/workflow/status/volopivoshenko/poetry-dotenv/CI?label=CI&logo=github">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/actions/workflows/deployment.yaml">\n    <img alt="deployment" src="https://img.shields.io/github/workflow/status/volopivoshenko/poetry-dotenv/CD?label=CD&logo=github">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/actions/workflows/codeql.yaml">\n    <img alt="codeql" src="https://img.shields.io/github/workflow/status/volopivoshenko/poetry-dotenv/CodeQL?label=codeQL&logo=github">\n  </a>\n  <a href="https://poetry-dotenv.readthedocs.io/en/latest">\n    <img alt="docs" src="https://img.shields.io/readthedocs/poetry-dotenv?logo=readthedocs">\n  </a>\n  <a href="https://pypi.org/project/poetry-dotenv">\n    <img alt="wheel" src="https://img.shields.io/pypi/wheel/poetry-dotenv?logo=pypi">\n  </a>\n</p>\n\n<p align="center">\n  <a href="https://codecov.io/gh/volopivoshenko/poetry-dotenv">\n    <img alt="coverage" src="https://img.shields.io/codecov/c/gh/volopivoshenko/poetry-dotenv?logo=codecov&token=yyck08xfTN"/>\n  </a>\n  <a href="https://lgtm.com/projects/g/volopivoshenko/poetry-dotenv/alerts/">\n    <img alt="alerts" src="https://img.shields.io/lgtm/alerts/github/volopivoshenko/poetry-dotenv?logo=lgtm"/>\n  </a>\n  <a href="https://lgtm.com/projects/g/volopivoshenko/poetry-dotenv/context:python">\n    <img alt="grade" src="https://img.shields.io/lgtm/grade/python/github/volopivoshenko/poetry-dotenv?logo=lgtm"/>\n  </a>\n  <a href="https://codeclimate.com/github/volopivoshenko/poetry-dotenv/maintainability">\n    <img alt="codeclimate" src="https://img.shields.io/codeclimate/maintainability/volopivoshenko/poetry-dotenv?logo=codeclimate">\n  </a>\n  <a href="https://pypi.org/project/poetry-dotenv">\n    <img alt="downloads" src="https://img.shields.io/pypi/dm/poetry-dotenv?logo=pypi">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/">\n    <img alt="stars" src="https://img.shields.io/github/stars/volopivoshenko/poetry-dotenv?logo=github">\n  </a>\n</p>\n\n<p align="center">\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/issues">\n    <img alt="issues" src="https://img.shields.io/github/issues/volopivoshenko/poetry-dotenv?logo=github">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/issues">\n    <img alt="issues" src="https://img.shields.io/github/issues-closed/volopivoshenko/poetry-dotenv?logo=github">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/pulls">\n    <img alt="pr" src="https://img.shields.io/github/issues-pr/volopivoshenko/poetry-dotenv?logo=github">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/pulls">\n    <img alt="pr" src="https://img.shields.io/github/issues-pr-closed/volopivoshenko/poetry-dotenv?logo=github">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/graphs/contributors">\n    <img alt="contributors" src="https://img.shields.io/github/contributors/volopivoshenko/poetry-dotenv?logo=github">\n  </a>\n  <a href="https://github.com/volopivoshenko/poetry-dotenv/commits/main">\n    <img alt="commit" src="https://img.shields.io/github/last-commit/volopivoshenko/poetry-dotenv?logo=github">\n  </a>\n</p>\n\n<p align="center">\n  <a href="https://www.buymeacoffee.com/volopivoshenko" target="_blank">\n    <img alt="buymeacoffee" src="https://img.shields.io/badge/buy_me_-a_coffee-ff6964?logo=buymeacoffee">\n  </a>\n</p>\n\n- [Overview](#overview)\n- [Installation](#installation)\n  - [Optional dependencies](#optional-dependencies)\n\n# Overview\n\n# Installation\n\n## Optional dependencies\n',
    'author': 'Volodymyr Pivoshenko',
    'author_email': 'volodymyr.pivoshenko@gmail.com',
    'maintainer': 'Volodymyr Pivoshenko',
    'maintainer_email': 'volodymyr.pivoshenko@gmail.com',
    'url': 'https://poetry-dotenv.readthedocs.io/en/latest',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
