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
    'version': '0.1.1',
    'description': 'Python package for easy data cleaning and wrangling operations.',
    'long_description': "# tydier\n\n`tydier` is a Python package that facilitates data cleaning and wrangling operations on `pandas` dataframes.\n\n- Project repo hosted on [GitHub](https://github.com/antobzzll/tydier).\n- Last version is [`0.1.1`](https://pypi.org/project/tydier/). Please refer to [CHANGELOG.md](https://github.com/antobzzll/tydier/blob/dev/CHANGELOG.md) for details on updates.\n\n## Installation\n\n```bash\n$ pip install tydier\n```\n\n## Usage\n\nFor complete usage examples please check the [example notebook](https://github.com/antobzzll/tydier/blob/dev/docs/example.ipynb).\n\n### Automatically **identify and fix** incorrect categorical variable values\n\n```python\nfrom tydier import catvars as catvars # for methods operating on categorical variables \nimport pandas as pd\n\ndirty_cats = ['monday', 'Tusday', 'Wednesday', 'thurda', 'Firday', 'saty', 'Sunday']\nclean_cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']\n\ndf = pd.DataFrame({'dirty_cats': dirty_cats, 'clean_cats': clean_cats})\n\ncatvars.find_inconsistent_categories(dirty_cats, clean_cats, mapping_dict=True)\n```\n```\n{'monday': 'Monday',\n 'Firday': 'Friday',\n 'thurda': 'Thursday',\n 'Tusday': 'Tuesday',\n 'saty': 'Saturday'}\n```\nPassing it to `pd.Series.replace()` will automatically replace inconsistent values with the correct predefined ones:\n```python\nmapping = catvars.find_inconsistent_categories(dirty_cats, clean_cats, mapping_dict=True)\ndf['cleaned_dirty_cats'] = df['dirty_cats'].replace(mapping)\ndf\n```\n|dirty_cats\t| clean_cats | cleaned_dirty_cats|\n| --- | ---| --- |\n| monday | Monday | Monday|\n| Tusday | Tuesday | Tuesday|\n| Wednesday | Wednesday | Wednesday|\n| thurda | Thursday | Thursday|\n| Firday | Friday | Friday|\n| saty | Saturday | Saturday|\n| Sunday | Sunday | Sunday|\n\n### Automatically transform into `float` a **currency `string` variable**, containing symbols and inconsistent spaces\n```python\nprices = pd.Series([' $50,    00', '30, 00€'])\nprint(numvars.currency_to_float(prices))\n```\n```\n0    50.0\n1    30.0\ndtype: float64\n```\n\n## Contributing\n\nInterested in contributing? Check out the [contributing guidelines](https://github.com/antobzzll/tydier/blob/dev/CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](https://github.com/antobzzll/tydier/blob/dev/CONDUCT.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`tydier` was created by [Antonio Buzzelli](https://github.com/antobzzll). It is licensed under the terms of the MIT license.\n\n## Credits\n\n`tydier` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the [`py-pkgs-cookiecutter` template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
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
