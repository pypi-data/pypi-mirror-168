# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['goats', 'goats.core', 'goats.eprem']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'netCDF4>=1.5.8,<2.0.0',
 'numpy>=1.21.4,<2.0.0',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'goats',
    'version': '0.0.28',
    'description': 'A set of tools for analyzing heliophysical datasets',
    'long_description': '# GOATS\n\nA set of tools for analyzing heliophysical datasets\n\nThe Generalized Observer Analysis Tool Set (GOATS) is a collection of objects that support interactive and scripted analysis of simulated and observed data in heliophysics.\n\n## Installation\n\n```bash\n$ pip install goats\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`goats` was created by Matt Young. It is licensed under the terms of the GNU General Public License v3.0 license.\n\n## Credits\n\n`goats` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Matt Young',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
