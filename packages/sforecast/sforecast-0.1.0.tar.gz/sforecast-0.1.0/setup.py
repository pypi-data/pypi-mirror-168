# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sforecast']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sforecast',
    'version': '0.1.0',
    'description': 'A package to support supervised learning forecast methods (ML and DL) within a sliding forecast framework (sliding window or expanding window)',
    'long_description': '# sforecast\n\nA package to support supervised learning forecast methods (ML and DL) within a sliding forecast framework (sliding or expanding window)\n\n## Installation\n\n```bash\n$ pip install sforecast\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`sforecast` was created by Alberto Gutierrez. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`sforecast` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n# sforecast\n',
    'author': 'Alberto Gutierrez',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
