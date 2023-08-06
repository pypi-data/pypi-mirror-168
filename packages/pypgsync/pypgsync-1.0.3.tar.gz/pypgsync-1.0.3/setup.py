# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypgsync']

package_data = \
{'': ['*']}

install_requires = \
['coverage-badge>=1.1.0,<2.0.0',
 'psycopg>=3.1.2,<4.0.0',
 'pytest-cov>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'pypgsync',
    'version': '1.0.3',
    'description': '',
    'long_description': '![test-badge](https://github.com/danielschweigert/pypgsync/actions/workflows/lint-and-test.yml/badge.svg)\n![coverage-badge](https://raw.githubusercontent.com/danielschweigert/pypgsync/main/coverage-manual.svg)\n\n# pypgsync\nPython utility to sync two postgresql databases\n\n\n## Installation\n\n```bash\npip install pypgsync\n```\n\n## Usage\nWith the goal to synchronize a destination database to the state of a source database, whereas the \nsource database grows in append-only fashion (no updates), the following steps can be run using \npypgsync:\n```python\nimport psycopg\nfrom pypgsync.pypgsync import sync\n\ncon_source = psycopg.connect(host="host_source", \n                             dbname="db_source", \n                             user="user_source", \n                             password="secret_source")\ncur_source = con_source.cursor()\n\ncon_destination = psycopg.connect(host="host_destination", \n                                  dbname="db_destination", \n                                  user="user_destination", \n                                  password="secret_destination")\n\nsync(cur_source, con_destination, tables=["table_a", "table_b", "table_c"], chunk_size=100)\n```',
    'author': 'Daniel Schweigert',
    'author_email': 'dan.schweigert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
