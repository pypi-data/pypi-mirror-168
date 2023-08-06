# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_mono_tools', 'py_mono_tools.backends', 'py_mono_tools.goals']

package_data = \
{'': ['*'], 'py_mono_tools': ['templates/*', 'templates/dockerfiles/*']}

install_requires = \
['click>=8,<9', 'pydocstyle[toml]>=6.1.1,<7.0.0']

extras_require = \
{':extra == "linters-python"': ['bandit>=1.7.4,<2.0.0',
                                'black>=22.8.0,<23.0.0',
                                'flake8>=5.0.4,<6.0.0',
                                'isort>=5.10.1,<6.0.0',
                                'mypy>=0.971,<0.972',
                                'pydocstringformatter>=0.7.2,<0.8.0',
                                'pylint>=2.15.2,<3.0.0'],
 ':extra == "testers-python"': ['pytest>=7.1.3,<8.0.0']}

entry_points = \
{'console_scripts': ['pmt = py_mono_tools.main:cli',
                     'py_mono_tools = py_mono_tools.main:cli']}

setup_kwargs = {
    'name': 'py-mono-tools',
    'version': '0.0.26',
    'description': 'A CLI designed to make it easier to work in a python mono repo',
    'long_description': 'For more information, please go the GitHub page. https://peterhoburg.github.io/py_mono_tools/\n',
    'author': 'Peter Hoburg',
    'author_email': 'peterHoburg@users.noreply.github.com',
    'maintainer': 'Peter Hoburg',
    'maintainer_email': 'peterHoburg@users.noreply.github.com',
    'url': 'https://peterhoburg.github.io/py_mono_tools/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
