# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labonneboite_common',
 'labonneboite_common.models',
 'labonneboite_common.tests']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.41,<2.0.0', 'Unidecode>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'labonneboite-common',
    'version': '0.2.0',
    'description': '',
    'long_description': "```\n _       _                            _           _ _\n| | __ _| |__   ___  _ __  _ __   ___| |__   ___ (_) |_ ___\n| |/ _` | '_ \\ / _ \\| '_ \\| '_ \\ / _ \\ '_ \\ / _ \\| | __/ _ \\\n| | (_| | |_) | (_) | | | | | | |  __/ |_) | (_) | | ||  __/\n|_|\\__,_|_.__/ \\___/|_| |_|_| |_|\\___|_.__/ \\___/|_|\\__\\___|\n```\n\n## About\n\nCommon library for labonneboite projects.\n\n\n## How tos\n\n### Tests\n\n```\nmake test### Getting started\n\n```\nmake init\n\n```\n\n```\n\n### Documentation\n\nThe documentation is based on [mkdocs](https://www.mkdocs.org/)\n\nTo open the docs:\n\n```\nmake documentation\n```\n\nIt will be accessible [here](http://127.0.0.1:9999/)\n",
    'author': 'La Bonne Boite',
    'author_email': 'labonneboite@pole-emploi.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/StartupsPoleEmploi/labonneboite-common',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
