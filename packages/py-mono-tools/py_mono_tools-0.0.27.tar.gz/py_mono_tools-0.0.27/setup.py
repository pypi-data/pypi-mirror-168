# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_mono_tools', 'py_mono_tools.backends', 'py_mono_tools.goals']

package_data = \
{'': ['*'], 'py_mono_tools': ['templates/*', 'templates/dockerfiles/*']}

install_requires = \
['click>=8,<9', 'pydocstyle[toml]>=6,<7']

extras_require = \
{':extra == "python" or extra == "python-linters" or extra == "all"': ['bandit>=1,<2',
                                                                       'black>=22,<23',
                                                                       'flake8>=5,<6',
                                                                       'isort>=5,<6',
                                                                       'mypy>=0,<1',
                                                                       'pydocstringformatter>=0.7,<0.8',
                                                                       'pylint>=2,<3'],
 ':extra == "python" or extra == "python-testers" or extra == "all"': ['pytest>=7,<8']}

entry_points = \
{'console_scripts': ['pmt = py_mono_tools.main:cli',
                     'py_mono_tools = py_mono_tools.main:cli']}

setup_kwargs = {
    'name': 'py-mono-tools',
    'version': '0.0.27',
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
