# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labonneboite_common',
 'labonneboite_common.models',
 'labonneboite_common.tests']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy<1.4', 'unidecode==0.4.21']

setup_kwargs = {
    'name': 'labonneboite-common',
    'version': '0.1.0',
    'description': '',
    'long_description': "```\n _       _                            _           _ _\n| | __ _| |__   ___  _ __  _ __   ___| |__   ___ (_) |_ ___\n| |/ _` | '_ \\ / _ \\| '_ \\| '_ \\ / _ \\ '_ \\ / _ \\| | __/ _ \\\n| | (_| | |_) | (_) | | | | | | |  __/ |_) | (_) | | ||  __/\n|_|\\__,_|_.__/ \\___/|_| |_|_| |_|\\___|_.__/ \\___/|_|\\__\\___|\n```\n\nCommon library for labonneboite projects.\n\nSee:\n- [labonneboite github](https://github.com/startupsPoleEmploi/labonneboite)\n- [labonneboite importer github](https://github.com/startupsPoleEmploi/lbb-importer)\n",
    'author': 'La Bonne Boite',
    'author_email': 'labonneboite@pole-emploi.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
