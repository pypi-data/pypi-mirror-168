# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_ado']

package_data = \
{'': ['*']}

install_requires = \
['azure-devops>=6.0.0-beta.4,<7.0.0',
 'importlib-metadata==4',
 'pytest-mock>=3.8.2,<4.0.0',
 'tox>=3.26.0,<4.0.0']

entry_points = \
{'flake8.extension': ['ADO = flake8_ado:Plugin']}

setup_kwargs = {
    'name': 'flake8-ado',
    'version': '0.2.0',
    'description': 'Flake8 plugin to check comments against AzureDevOps ticket references.',
    'long_description': '# flake-aod\n\nFlake8 extension to check comments against Azure DevOps tickets. The plugin checks that:\n1. Every comment with a reference to an ADO item (`AB#12345`) has a corresponding item.\n2. ADO items are references in a proper format (`ADO: AB#12345`)\n3. TODO items with ADO annotation have assigned item (`TODO: AB#12345`).\n\nExample:\n```python\nclass Foo:\n    def foo(self) -> None: # TODO: AB#12345\n        pass # ab 12345\n```\n```bash\n>> flake8\n\n```',
    'author': 'DanielKusyDev',
    'author_email': 'daniel.kusy97@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DanielKusyDev/flake8-ado',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
