# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eralchemy2']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.41,<2.0.0', 'pygraphviz>=1.7,<2.0']

entry_points = \
{'console_scripts': ['eralchemy2 = eralchemy2.main:cli']}

setup_kwargs = {
    'name': 'eralchemy2',
    'version': '1.3.4',
    'description': 'Simple entity relation (ER) diagrams generation',
    'long_description': '\n[![PyPI Version](https://img.shields.io/pypi/v/eralchemy2.svg)](\nhttps://pypi.org/project/eralchemy2/)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/eralchemy2.svg)](\nhttps://pypi.org/project/eralchemy2/)\n![Github Actions](https://github.com/maurerle/eralchemy2/actions/workflows/python-app.yml/badge.svg)\n\n\n# Entity relation diagrams generator\n\neralchemy2 generates Entity Relation (ER) diagram (like the one below) from databases or from SQLAlchemy models.\nWorks with SQLAlchemy < 1.4 but also with versions greater than 1.4\n\n## Example\n\n![Example for a graph](https://raw.githubusercontent.com/maurerle/eralchemy2/main/newsmeme.svg?raw=true "Example for NewsMeme")\n\n[Example for NewsMeme](https://bitbucket.org/danjac/newsmeme)\n\n## Quick Start\n\n### Install\nTo install eralchemy2, just do:\n\n    $ pip install eralchemy2\n\n`eralchemy2` requires [GraphViz](http://www.graphviz.org/download) to generate the graphs and Python. Both are available for Windows, Mac and Linux.\n\n### Usage from Command Line\n\n#### From a database\n\n    $ eralchemy2 -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.pdf\n\nThe database is specified as a [SQLAlchemy](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#database-urls)\ndatabase url.\n\n#### From a markdown file.\n\n    $ curl \'https://raw.githubusercontent.com/maurerle/eralchemy2/main/example/newsmeme.er\' > markdown_file.er\n    $ eralchemy2 -i \'markdown_file.er\' -o erd_from_markdown_file.pdf\n\n#### From a Postgresql DB to a markdown file excluding tables named `temp` and `audit`\n\n    $ eralchemy2 -i \'postgresql+psycopg2://username:password@hostname:5432/databasename\' -o filtered.er --exclude-tables temp audit\n\n#### From a Postgresql DB to a markdown file excluding columns named `created_at` and `updated_at` from all tables\n\n    $ eralchemy2 -i \'postgresql+psycopg2://username:password@hostname:5432/databasename\' -o filtered.er --exclude-columns created_at updated_at\n\n#### From a Postgresql DB to a markdown file for the schema `schema`\n\n    $ eralchemy2 -i \'postgresql+psycopg2://username:password@hostname:5432/databasename\' -s schema\n\n### Usage from Python\n\n```python\nfrom eralchemy2 import render_er\n## Draw from SQLAlchemy base\nrender_er(Base, \'erd_from_sqlalchemy.png\')\n\n## Draw from database\nrender_er("sqlite:///relative/path/to/db.db", \'erd_from_sqlite.png\')\n```\n\n## Architecture\n![Architecture schema](https://raw.githubusercontent.com/maurerle/eralchemy2/main/eralchemy_architecture.png?raw=true "Architecture schema")\n\nThanks to it\'s modular architecture, it can be connected to other ORMs/ODMs/OGMs/O*Ms.\n\n## Contribute\n\nEvery feedback is welcome on the [GitHub issues](https://github.com/maurerle/eralchemy2/issues).\n\nTo run the tests, use : `$ py.test` or `$ tox`.\nSome tests require a local postgres database with a schema named test in a database\nnamed test all owned by a user named eralchemy with a password of eralchemy.\nThis can be easily set up using docker-compose with: `docker-compose up -d`.\n\nAll tested PR are welcome.\n\n## Notes\n\neralchemy2 is a fork of its predecessor [ERAlchemy](https://github.com/Alexis-benoist/eralchemy) by @Alexis-benoist, which is not maintained anymore and does not work with SQLAlchemy > 1.4.\nIf it is maintained again, I\'d like to push the integrated changes upstream.\n\nERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd), though it is able to render the ER diagram directly\nfrom the database and not just only from the `ER` markup language.\n\nReleased under an Apache License 2.0\n\nInitial Creator: Alexis Benoist [Alexis_Benoist](https://twitter.com/Alexis_Benoist)\n',
    'author': 'Florian Maurer',
    'author_email': 'fmaurer@disroot.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/maurerle/eralchemy2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
