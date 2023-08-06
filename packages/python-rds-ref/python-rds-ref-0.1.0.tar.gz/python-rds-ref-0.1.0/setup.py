# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_rds_ref']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dataserver = python_rds_ref.dataserver:cli']}

setup_kwargs = {
    'name': 'python-rds-ref',
    'version': '0.1.0',
    'description': '',
    'long_description': '# PYTHON RDS REF Implementation\n\nThis is a simple python remote dataset server implementation that should work at serving up files to spec with the DCP RDS Requirements.\n\n\n',
    'author': 'Hamada Gasmallah',
    'author_email': 'hamada@distributive.network',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
