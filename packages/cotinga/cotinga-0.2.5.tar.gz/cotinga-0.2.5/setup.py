# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cotinga',
 'cotinga.core',
 'cotinga.gui',
 'cotinga.gui.core',
 'cotinga.gui.core.list_manager',
 'cotinga.gui.dialogs',
 'cotinga.gui.dialogs.doc_setup',
 'cotinga.gui.pages',
 'cotinga.gui.pages.panels',
 'cotinga.models']

package_data = \
{'': ['*'],
 'cotinga': ['data/*',
             'data/default/*',
             'data/default/doc_setup/*',
             'data/flags/*',
             'data/icons/*',
             'data/locale/*',
             'data/locale/en_US/LC_MESSAGES/*',
             'data/locale/fr_FR/LC_MESSAGES/*']}

install_requires = \
['Babel>=2.9.1,<3.0.0',
 'microlib>=1.8.0,<2.0.0',
 'pikepdf>=5.0.1,<6.0.0',
 'pygobject>=3.42,<4.0',
 'python-magic>=0.4.25,<0.5.0',
 'reportlab>=3.6.7,<4.0.0',
 'sqlalchemy-utils>=0.38.2,<0.39.0',
 'sqlalchemy>=1.4.31,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'wheel>=0.37.1,<0.38.0']

entry_points = \
{'console_scripts': ['cotinga = cotinga:run']}

setup_kwargs = {
    'name': 'cotinga',
    'version': '0.2.5',
    'description': "Teachers' helper to manage their pupils' progression.",
    'long_description': "\n\nOverview\n========\n\nCotinga helps teachers to manage their pupils' progression.\n\nDocumentation\n=============\n\nA user guide is available `here <https://cotinga.readthedocs.io/en/latest/index.html>`__.\n\nCredits\n=======\n\nFlags are from:\nhttps://github.com/fonttools/region-flags/\n",
    'author': 'Nicolas Hainaux',
    'author_email': 'nh.techn@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nicolas.hainaux/cotinga',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
