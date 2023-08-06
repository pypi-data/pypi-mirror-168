# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ols_py']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'requests>=2.0,<3.0']

setup_kwargs = {
    'name': 'ols-py',
    'version': '0.0.3',
    'description': 'Python client for the Ontology Lookup Service',
    'long_description': "# ols-py\n\n[![PyPI](https://img.shields.io/pypi/v/ols-py?style=flat-square)](https://pypi.python.org/pypi/ols-py/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ols-py?style=flat-square)](https://pypi.python.org/pypi/ols-py/)\n[![PyPI - License](https://img.shields.io/pypi/l/ols-py?style=flat-square)](https://pypi.python.org/pypi/ols-py/)\n[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)\n\n\n---\n\n**Documentation**: [https://ahida-development.github.io/ols-py](https://ahida-development.github.io/ols-py)\n\n**Source Code**: [https://github.com/ahida-development/ols-py](https://github.com/ahida-development/ols-py)\n\n**PyPI**: [https://pypi.org/project/ols-py/](https://pypi.org/project/ols-py/)\n\n---\n\nPython client for the Ontology Lookup Service\n\n## Installation\n\n```sh\npip install ols-py\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.10+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings\n of the public signatures of the source code. The documentation is updated and published as a [Github project page\n ](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/ahida-development/ols-py/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/ahida-development/ols-py/releases) and publish it. When\n a release is published, it'll trigger [release](https://github.com/ahida-development/ols-py/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n\nThis project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.\n",
    'author': 'Marius Mather',
    'author_email': 'marius.mather@sydney.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ahida-development.github.io/ols-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.1,<4.0',
}


setup(**setup_kwargs)
