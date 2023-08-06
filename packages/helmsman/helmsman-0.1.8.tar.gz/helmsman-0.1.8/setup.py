# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['helmsman']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'jmespath>=0.10.0,<0.11.0', 'py-linq>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['helmsman = helmsman.cli:main']}

setup_kwargs = {
    'name': 'helmsman',
    'version': '0.1.8',
    'description': 'Helmsman is a test framework for helm',
    'long_description': '\n# Helmsman\n\n\n<div align="center">\n\n[![PyPI - Version](https://img.shields.io/pypi/v/helmsman.svg)](https://pypi.python.org/pypi/helmsman)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/helmsman.svg)](https://pypi.python.org/pypi/helmsman)\n[![Tests](https://github.com/mrlyc/helmsman/workflows/tests/badge.svg)](https://github.com/mrlyc/helmsman/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/mrlyc/helmsman/branch/main/graph/badge.svg)](https://codecov.io/gh/mrlyc/helmsman)\n[![Read the Docs](https://readthedocs.org/projects/helmsman/badge/)](https://helmsman.readthedocs.io/)\n[![PyPI - License](https://img.shields.io/pypi/l/helmsman.svg)](https://pypi.python.org/pypi/helmsman)\n\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)\n\n</div>\n\n\nHelmsman is a test framework for helm\n\n\n* GitHub repo: <https://github.com/mrlyc/helmsman.git>\n* Documentation: <https://helmsman.readthedocs.io>\n* Free software: MIT\n\n\n## Features\n\n* TODO\n\n## Quickstart\n\nTODO\n\n## Credits\n\nThis package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.\n\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage\n',
    'author': 'MrLYC',
    'author_email': 'imyikong@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrlyc/helmsman',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
