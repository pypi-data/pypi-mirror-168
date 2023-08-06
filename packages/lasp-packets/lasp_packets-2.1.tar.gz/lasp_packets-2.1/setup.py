# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lasp_packets']

package_data = \
{'': ['*']}

install_requires = \
['bitstring>=3.0.0']

setup_kwargs = {
    'name': 'lasp-packets',
    'version': '2.1',
    'description': 'CCSDS packet decoding library',
    'long_description': 'None',
    'author': 'Gavin Medley',
    'author_email': 'gavin.medley@lasp.colorado.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
