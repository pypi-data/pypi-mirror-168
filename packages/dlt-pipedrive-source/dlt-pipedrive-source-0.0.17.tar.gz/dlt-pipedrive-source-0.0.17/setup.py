# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlt_pipedrive_source']

package_data = \
{'': ['*'], 'dlt_pipedrive_source': ['sample_data/*']}

install_requires = \
['google-cloud-bigquery',
 'psycopg2-binary',
 'python-dlt>=0.1.0rc10',
 'python-pipedrive==0.4.0']

setup_kwargs = {
    'name': 'dlt-pipedrive-source',
    'version': '0.0.17',
    'description': '',
    'long_description': '# dlt-pipedrive-source\n\nprototype for source creation\n\n\n# Parent tables \n`\'deal\', \'deal_participant\', \'deal_flow\'`\n\n\n# Usage\n\noptionally Create a virtual environment\n```\npython3 -m venv ./dlt_pipedrive_env\nsource ./dlt_pipedrive_env/bin/activate\n```\n\ninstall library\n\n```pip install dlt-pipedrive-source```\n\nIf the library cannot be found, ensure you have the required python version as per the `pyproject.toml`file.\n(3.8+)\n\nYou can run the snippet file below to load a sample data set. \nYou would need to add your target credentials first.\ncopy the file below and add credentials, then run it\n\n\n[run_load.py](run_load.py)\n```python run_load.py```\n\nIf you want only some of the tables, pass them as an argument in the tables list in the loader (see below)\n```\n# of all tables, get only deal_participant\ntables = [\'deal_participant\'] \n# get all tables\ntables = [] \n\nYou can also toggle "mock data" to True in the load function, or pass None credentials, to try mock sample data.',
    'author': 'Adrian Brudaru',
    'author_email': 'adrian@scalevector.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
