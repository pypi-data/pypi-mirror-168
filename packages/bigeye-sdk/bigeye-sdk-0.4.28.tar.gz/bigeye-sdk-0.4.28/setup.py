# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigeye_sdk',
 'bigeye_sdk.authentication',
 'bigeye_sdk.bigconfig_validation',
 'bigeye_sdk.class_ext',
 'bigeye_sdk.client',
 'bigeye_sdk.controller',
 'bigeye_sdk.decorators',
 'bigeye_sdk.exceptions',
 'bigeye_sdk.functions',
 'bigeye_sdk.generated',
 'bigeye_sdk.generated.com',
 'bigeye_sdk.generated.com.torodata',
 'bigeye_sdk.generated.com.torodata.models',
 'bigeye_sdk.generated.google',
 'bigeye_sdk.log',
 'bigeye_sdk.model']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub==1.54.1',
 'PyYAML>=6.0,<7.0',
 'betterproto>=1.2.5,<2.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'grpclib>=0.4.2,<0.5.0',
 'keyring==23.2.1',
 'lz4>=4.0.1,<5.0.0',
 'pycryptodomex==3.11.0',
 'pydantic-yaml>=0.8.0,<0.9.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'requests>=2.28.1,<3.0.0',
 'setuptools>=59.6.0,<60.0.0',
 'smart-open>=6.1.0,<7.0.0',
 'types-PyYAML>=6.0.11,<7.0.0']

setup_kwargs = {
    'name': 'bigeye-sdk',
    'version': '0.4.28',
    'description': 'Bigeye SDK offers developer tools and clients to interact with Bigeye programmatically.',
    'long_description': '# Bigeye SDK\n\nBigeye SDK is a collection of protobuf generated code, functions, and models used to interact programmatically\nwith the Bigeye API.  Bigeye currently supports a Python SDK.  The main entry point is the DatawatchClient \nabstraction and, in this core package, a basic auth client has been implemented.  The abstract base class \nincludes core functionality (methods to interact with the API) and each implementation should enable a \ndifferent authorization methods.\n\n## Install\n\n```shell\npip install bigeye_sdk\n```\n\n## Basic Auth\n\nBasic authorization credentials can be stored as Json either on disk or in a secrets/credentials manager.  This\nformat will be marshalled into an instance of [BasicAuthRequestLibApiConf](bigeye_sdk/authentication/api_authentication.py).\n\n```json\n{\n    "base_url": "https://app.bigeye.com",\n    "user": "",\n    "password": ""\n}\n```\n',
    'author': 'Bigeye',
    'author_email': 'support@bigeye.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://docs.bigeye.com/docs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
