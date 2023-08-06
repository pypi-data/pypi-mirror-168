# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['difai']

package_data = \
{'': ['*']}

install_requires = \
['nbformat>=5.6.0,<6.0.0', 'pip-tools>=6.8.0,<7.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['difai = difai.main:app']}

setup_kwargs = {
    'name': 'difai',
    'version': '0.1.0',
    'description': "'Did I forget any imports' generates requirement files for you",
    'long_description': '# Did I forget any imports?\n\nDIFAI searches for import statements for all the python and jupyter notebook files in the current directory. It then uses `pip freeze` to get your installed versions and `pip-compile` to generate a `requirements.txt` file containing all of your dependencies and their depdendencies including hashes for a reproducible build. \n\n## Pipeline\n\n```mermaid\ngraph TB\n    A[glob] --> B\n    A --> C\n    B[.py] --> D\n    C[.ipynb] -->|nbconvert| B\n    D[AST]  --> E\n    X[pip freeze] --> E\n    E[requirements.in] -->|pip tools| F\n    F[requirements.txt]\n```\n\n\n',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'Marvin van Aalst',
    'maintainer_email': 'marvin.vanaalst@gmail.com',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
