# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tydier']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'tydier',
    'version': '0.1.0',
    'description': 'Python package for cleaning and manipulating data.',
    'long_description': '# tydier\n\n`tydier` is a Python package that facilitates data cleaning and wrangling operations on `pandas` dataframes.\n\n## Installation\n\n`tydier` is still in its early development phase; a first version has not been released yet. Please stay tuned ... or feel free to contribute to speed up the release process!\n\n<!-- ```bash\n$ pip install tydier\n``` -->\n\n## Usage\n\nFor usage examples please check the [example notebook](./docs/example.ipynb).\n\n## Contributing\n\nInterested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`tydier` was created by Antonio Buzzelli. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`tydier` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Antonio Buzzelli',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
