# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shipyard',
 'shipyard.api',
 'shipyard.api.v1',
 'shipyard.cli',
 'shipyard.colony',
 'shipyard.deploy',
 'shipyard.envoy',
 'shipyard.vigil']

package_data = \
{'': ['*']}

install_requires = \
['docker[ssh]>=5.0.3,<6.0.0',
 'fastapi>=0.79.0,<0.80.0',
 'gunicorn>=20.1.0,<21.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'sqlmodel>=0.0.8,<0.0.9',
 'typer[all]>=0.6.1,<0.7.0',
 'uvicorn[standard]>=0.18.2,<0.19.0']

entry_points = \
{'console_scripts': ['shipyard = shipyard.cli.main:app']}

setup_kwargs = {
    'name': 'shipyard-urbit',
    'version': '0.1.3',
    'description': 'Urbit hosting and automation platform',
    'long_description': '# Shipyard\n\nUrbit hosting and automation platform.\n\nNote: this is a Pre-Release package.  All changes will be breaking.  Wait for release 1.0.0 or later.\n\n## Install\n\n```\npip install shipyard-urbit\n```\n\n## Usage\n\n```\nshipyard\n```\n\nTo use the application locally, run `shipyard api` and visit `localhost:8000`.\n\nFor multi-user production deploymenrs, or any other custom configuration, use `shipyard gunicorn` passing Gunicorn server options ([Reference](https://docs.gunicorn.org/en/stable/settings.html)).  Omit the `wsgi_app` argument and `worker_class` option as these are preconfigured by shipyard.\n\n## Configuration\n\nSpecify the following environment vars to configure your application.  You may use a `.env` file in the location where `shipyard` is run.\n\n- `SHIPYARD_DATA_DIR` - directory where SQLite database and other data will live, default: `~/.shipyard/`\n    -  Override at runtime using the `--data-dir` option. Global command line options must come before the application command, example: `shipyard --data-dir=mydir api`\n- `SHIPYARD_SQLITE_FILENAME` - name of the db file within the data directory, default: `shipyard.db`\n- `SHIPYARD_POSTGRES_URL` - PostgreSQL connection string to override use of SQLite, default: `None`\n\nPostgreSQL is only recommended for large multi-user deployments. You must create your database before connecting with shipyard like so:\n\n```\nCREATE DATABASE shipyard;\n```\n\nThen `SHIPYARD_POSTGRES_URL` should look something like this:\n\n```\npostgresql://user:password@127.0.0.1:5432/shipyard\n```\n\n## API Overview\n\nVisit [redacted] for full API Documentation.\n\n## Development\n\n### Modules\n\n#### shipyard\n\n * `db.py` - database engine for SQLite/PostreSQL application state\n * `models.py` - types used throughout the project\n * `settings.py` - system-wide settings and env vars\n * `tasks.py` - for running background jobs or long running processes\n\n#### shipyard.api\n\nHTTP API built with FastAPI.\n\n#### shipyard.cli\n\nCommand-line interface built with Typer.\n\n#### shipyard.colony\n\nHost setup and configuration using Ansible.\n\n#### shipyard.deploy\n\nCreating and migrating Urbit ships within our host infrastructure.\n\n#### shipyard.envoy\n\nCommunication and direction of Urbit ships.\n\n#### shipyard.vigil\n\nMonitoring and alerting. WIP.\n\n## License\n\nThis project is licensed under Apache-2.0.  Code licensed from other projects will be clearly marked with the appropriate notice.\n',
    'author': 'nodreb-borrus',
    'author_email': 'nodreb@borr.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
