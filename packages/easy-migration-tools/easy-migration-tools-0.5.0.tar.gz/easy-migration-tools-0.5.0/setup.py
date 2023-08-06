# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['easymigration', 'easymigration.scripts']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'bs4>=0.0.1,<0.0.2',
 'requests>=2.26.0,<3.0.0',
 'ri>=0.1,<0.2']

entry_points = \
{'console_scripts': ['list-bagstore-files = '
                     'easymigration.scripts.list_bagstore_files:main',
                     'update-thematische-collecties = '
                     'easymigration.scripts.update_thematische_collecties:main']}

setup_kwargs = {
    'name': 'easy-migration-tools',
    'version': '0.5.0',
    'description': 'Utility scripts for the migration from EASY to Data Stations',
    'long_description': None,
    'author': 'DANS-KNAW',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
