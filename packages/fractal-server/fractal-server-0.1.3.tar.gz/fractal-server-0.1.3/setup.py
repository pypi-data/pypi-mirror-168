# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fractal_server',
 'fractal_server.app',
 'fractal_server.app.api',
 'fractal_server.app.api.v1',
 'fractal_server.app.db',
 'fractal_server.app.models',
 'fractal_server.app.runner',
 'fractal_server.app.security',
 'fractal_server.migrations',
 'fractal_server.migrations.versions']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.38.3,<0.39.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'alembic>=1.8.0,<2.0.0',
 'fastapi-users-db-sqlmodel>=0.2.0,<0.3.0',
 'fastapi-users[oauth]>=10.1.1,<11.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'fractal-client<1.0.0',
 'parsl>=1.3.0dev0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'sqlmodel>=0.0.8,<0.0.9',
 'uvicorn>=0.18.2,<0.19.0']

extras_require = \
{'tasks-core': ['fractal-tasks-core>=0.1.4,<0.2.0']}

entry_points = \
{'console_scripts': ['fractal-server = fractal_server.__main__:run']}

setup_kwargs = {
    'name': 'fractal-server',
    'version': '0.1.3',
    'description': 'Server component of the Fractal analytics platform',
    'long_description': '# Fractal Server\n\n[![PyPI version](https://badge.fury.io/py/fractal-server.svg)](https://badge.fury.io/py/fractal-server)\n\nFractal is a framework to process high content imaging data at scale and prepare it for interactive visualization.\n\nThis is the server component of the fractal analytics platform. If you are interested in the client component, please refer to the [main\nrepository](https://github.com/fractal-analytics-platform/fractal). If you are interested in the fractal tasks, please refer to [the tasks repository](https://github.com/fractal-analytics-platform/fractal-tasks-core).\n\n## Installation\n\nYou may\n`pip install fractal-server`\n\nThis will install the project and its dependencies. If you wish to also install\nFractal core tasks, use\n```\npip install fractal-server[core-tasks]\n```\n\n### Environment and database\n\nYou will need to define some environment variables in order to use\n`fractal-server`. For your convenience, you may simply copy\n`template.fractal_server.env` to `.fractal_server.env`.\n\n`fractal-server` requires a database to run. Once you set up the environment\nvariables you need to initialise the database by invoking\n\n```\nalembic upgrade head\n```\n\nNOTE: as `fractal-server` is still in pre-alpha the database schema is not yet\ncommitted to the repository. As such you\'ll be required to first create a\nschema revision with `alembic revision --autogenerate -m "[your commit\nmessage]"`.\n\n## Contributing\n\nTo contribute to the development of `fractal-server` you may fork and clone the\n[repository](https://github.com/fractal-analytics-platform/fractal-server).\n\nWe use [poetry](https://python-poetry.org/docs/) (v1.2) to manage the\ndevelopment environment and the dependencies. Running\n\n```\npoetry install [--with dev]\n```\n\nwill take care of installing all the dependencies in a separate environment,\noptionally installing also the development dependencies.\n\nIt may be useful to use a different interpreter from the one installed in your\nsystem. To this end we recommend using\n[pyenv](https://github.com/pyenv/pyenv). In the project folder, invoking\n\n```\npyenv local 3.8.13\npoetry env use 3.8\npoetry install\n```\n\nwill install Fractal in a development environment using `python 3.8.13` instad\nof the system-wide interpreter.\n\n### Testing\n\nWe use [pytest](https://docs.pytest.org/en/7.1.x/) for unit and integration\ntesting of Fractal. If you installed the development dependencies, you may run\nthe test suite by invoking\n\n```\npoetry run pytest\n```\n\n## Contributors\n\nFractal was conceived in the Liberali Lab at the Friedrich Miescher Institute\nfor Biomedical Research and in the Pelkmans Lab at the University of Zurich\n(both in Switzerland). The project lead is with\n[@gusqgm](https://github.com/gusqgm) & [@jluethi](https://github.com/jluethi).\nThe core development is done under contract by\n[@mfranzon](https://github.com/mfranzon), [@tcompa](https://github.com/tcompa)\n& [@jacopo-exact](https://github.com/jacopo-exact) from [eXact lab\nS.r.l.](https://exact-lab.it).\n\n## License\n\nFractal is released according to a BSD 3-Clause License. See `LICENSE`.\n',
    'author': 'Jacopo Nespolo',
    'author_email': 'jacopo.nespolo@exact-lab.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fractal-analytics-platform/fractal-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
