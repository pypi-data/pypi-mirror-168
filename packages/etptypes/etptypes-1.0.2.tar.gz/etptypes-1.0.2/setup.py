# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etptypes',
 'etptypes.energistics',
 'etptypes.energistics.etp',
 'etptypes.energistics.etp.v12',
 'etptypes.energistics.etp.v12.datatypes',
 'etptypes.energistics.etp.v12.datatypes.channel_data',
 'etptypes.energistics.etp.v12.datatypes.data_array_types',
 'etptypes.energistics.etp.v12.datatypes.object',
 'etptypes.energistics.etp.v12.private_protocols',
 'etptypes.energistics.etp.v12.private_protocols.witsml_soap',
 'etptypes.energistics.etp.v12.protocol',
 'etptypes.energistics.etp.v12.protocol.channel_data_frame',
 'etptypes.energistics.etp.v12.protocol.channel_data_load',
 'etptypes.energistics.etp.v12.protocol.channel_streaming',
 'etptypes.energistics.etp.v12.protocol.channel_subscribe',
 'etptypes.energistics.etp.v12.protocol.core',
 'etptypes.energistics.etp.v12.protocol.data_array',
 'etptypes.energistics.etp.v12.protocol.dataspace',
 'etptypes.energistics.etp.v12.protocol.discovery',
 'etptypes.energistics.etp.v12.protocol.discovery_query',
 'etptypes.energistics.etp.v12.protocol.growing_object',
 'etptypes.energistics.etp.v12.protocol.growing_object_notification',
 'etptypes.energistics.etp.v12.protocol.growing_object_query',
 'etptypes.energistics.etp.v12.protocol.store',
 'etptypes.energistics.etp.v12.protocol.store_notification',
 'etptypes.energistics.etp.v12.protocol.store_query',
 'etptypes.energistics.etp.v12.protocol.supported_types',
 'etptypes.energistics.etp.v12.protocol.transaction']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1,<2', 'typingx>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'etptypes',
    'version': '1.0.2',
    'description': 'ETP python dev kit',
    'long_description': '# Etptypes\n\n[![License](https://img.shields.io/pypi/l/etptypes)](https://github.com/geosiris-technologies/etptypes-python/blob/main/LICENSE)\n![Python version](https://img.shields.io/pypi/pyversions/etptypes)\n[![PyPI](https://img.shields.io/pypi/v/etptypes)](https://badge.fury.io/py/etptypes)\n\n\n## Introduction\n\nETP python dev kit\n\n## Requirements\n\n- python ^3.8\n- pydantic ~1\n- typingx ^0.6.0\n\n## Version History\n\n- 1.0.1: \n    - Initial Release\n- 1.0.2: \n    - Bug fix for ETP array deserialisation\n\n## License\n\nThis project is licensed under the Apache 2.0 License - see the `LICENSE` file for details\n\n## Support\n\nPlease enter an issue in the repo for any questions or problems.\n',
    'author': 'Lionel Untereiner',
    'author_email': 'lionel.untereiner@geosiris.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://www.geosiris.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
