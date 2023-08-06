# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taktile_client',
 'taktile_client.arrow',
 'taktile_client.arrow.serialize',
 'taktile_client.rest',
 'taktile_client.rest.serialize']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'setuptools>=0.0.0',
 'taktile-types>=0.17.0,<1.0.0',
 'tenacity>=8.0.1,<9.0.0']

extras_require = \
{'arrow': ['numpy>=1.23,<2.0',
           'pandas>=1.4,<2.0',
           'pyarrow>=9.0,<10.0',
           'certifi==2021.10.8']}

setup_kwargs = {
    'name': 'taktile-client',
    'version': '1.0.5',
    'description': 'A lightweight client to call models deployed on Taktile.',
    'long_description': '# Taktile Client\n\n[![pypi status](https://img.shields.io/pypi/v/taktile-client.svg)](https://pypi.python.org/pypi/taktile-client)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)\n\nTaktile enables data science teams to industrialize, scale, and maintain machine learning models. Our ML development platform makes it easy to create your own end-to-end ML applications:\n\n- Turn models into auto-scaling APIs in a few lines of code\n- Easily add model tests\n- Create and share model explanations through the Taktile UI\n\n`taktile-client` is a stand-alone python client which can be used to make requests to Taktile deployments via REST or [Arrow Flight](https://arrow.apache.org/docs/format/Flight.html). If you require the full Taktile dev tooling, consider installing [taktile-cli](https://pypi.org/project/taktile-cli/) instead. Find more information in our [docs](https://docs.taktile.com).\n\nTo install the REST client only, run `pip install taktile-client`. For both REST and Arrow, run `pip install taktile-client\\[arrow]`.\n',
    'author': 'Taktile GmbH',
    'author_email': 'devops@taktile.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
