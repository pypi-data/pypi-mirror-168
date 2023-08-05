# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dexa_protocol',
 'dexa_protocol.v1_0',
 'dexa_protocol.v1_0.handlers',
 'dexa_protocol.v1_0.messages',
 'dexa_protocol.v1_0.messages.marketplace',
 'dexa_protocol.v1_0.messages.negotiation',
 'dexa_protocol.v1_0.models',
 'dexa_protocol.v1_0.routes',
 'dexa_protocol.v1_0.routes.maps',
 'dexa_protocol.v1_0.routes.openapi']

package_data = \
{'': ['*']}

install_requires = \
['acapy-patched==0.5.6-dev1', 'dexa-sdk==0.1.8']

setup_kwargs = {
    'name': 'dexa-protocol',
    'version': '0.1.6',
    'description': 'Hosts Data Disclosure Agreement protocols',
    'long_description': '<h1 align="center">\n    Data Exchange Agreements (DEXA) Protcol Implementation\n</h1>\n\n<p align="center">\n    <a href="/../../commits/" title="Last Commit"><img src="https://img.shields.io/github/last-commit/decentralised-dataexchange/dexa-protocol?style=flat"></a>\n    <a href="/../../issues" title="Open Issues"><img src="https://img.shields.io/github/issues/decentralised-dataexchange/dexa-protocol?style=flat"></a>\n    <a href="./LICENSE" title="License"><img src="https://img.shields.io/badge/License-Apache%202.0-green.svg?style=flat"></a>\n</p>\n\n<p align="center">\n  <a href="#about">About</a> •\n  <a href="#release-status">Release Status</a> •\n  <a href="#contributing">Contributing</a> •\n  <a href="#licensing">Licensing</a>\n</p>\n\n## About\n\nThis repository hosts source code for DEXA didcomm protocol plugin for aca-py. This is part of the deliverables for Provenance services with smart data agreement ([PS-SDA](https://ontochain.ngi.eu/content/ps-sda)) project that has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 957338. \n## Release Status\n\nNot released, work in progress. Planned release: September 2022\n## Contributing\n\nFeel free to improve the plugin and send us a pull request. If you found any problems, please create an issue in this repo.\n\n## Licensing\nCopyright (c) 2022-25 LCubed AB (iGrant.io), Sweden\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.\n\nYou may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.\n\nUnless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the LICENSE for the specific language governing permissions and limitations under the License.',
    'author': 'George J Padayatti',
    'author_email': 'george.padayatti@igrant.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decentralised-dataexchange/dexa-protocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
