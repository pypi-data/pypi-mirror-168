# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['project_maker', 'project_maker.maker']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.4,<2.0.0',
 'black>=22.8.0,<23.0.0',
 'isort>=5.10.1,<6.0.0',
 'rich>=12.5.1,<13.0.0',
 'tomlkit>=0.11.4,<0.12.0']

entry_points = \
{'console_scripts': ['project_maker = model_w.project_maker.__main__:__main__']}

setup_kwargs = {
    'name': 'modelw-project-maker',
    'version': '1.0.0a1',
    'description': 'A tool to create Model-W-compliant projects',
    'long_description': 'None',
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
