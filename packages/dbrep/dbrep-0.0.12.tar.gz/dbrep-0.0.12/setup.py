# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbrep', 'dbrep.conversions', 'dbrep.engines', 'dbrep.engines.experimental']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.0', 'SQLAlchemy>=1.4.40,<2.0.0', 'cryptography>=37.0.4,<38.0.0']

entry_points = \
{'console_scripts': ['dbrep = dbrep.cli:cli_dbrep']}

setup_kwargs = {
    'name': 'dbrep',
    'version': '0.0.12',
    'description': 'Package to sync tables across DBs, i.e. EL in ELT/ETL',
    'long_description': "# dbrep\nPackage to sync tables across DBs, i.e. EL in ELT/ETL\n\n## What it is\nIt is tool for loading data from one DB and uploading into another. That is it. It is the simplest EL-tool.\n\n## What it is NOT\n- It is NOT orchestrator. You may use existing one, like Airflow, Prefect or Dagster.\n- It is NOT data transformation tool. You may use DBT or others.\n- It is NOT data ingestion tool -- it won't grab data from external resources.\n\n## Distinctive features\n### Simple\nIt does not try to solve miriad of problems, but nicely fits into existing data-engineering stack with (airflow, dbt and other tools).\n\n### Stateless\nIt does not store state of jobs or tables, besides connection configs.\n\n### Robust\nSince it is stateless there is only a handful of things that could go wrong.\n\n### Type-aware\nTypes are not lost in translation. I.e. if it was a *number(10,0)* in Oracle, it won't suddenly become a *Float64* in ClickHouse.",
    'author': 'Valentin  Stepanovich',
    'author_email': 'kolhizin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
