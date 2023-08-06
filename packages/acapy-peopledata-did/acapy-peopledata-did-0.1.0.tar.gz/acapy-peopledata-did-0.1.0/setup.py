# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peopledata_did',
 'peopledata_did.patched_protocols',
 'peopledata_did.patched_protocols.issue_credential',
 'peopledata_did.patched_protocols.issue_credential.v1_0',
 'peopledata_did.patched_protocols.issue_credential.v1_0.handlers',
 'peopledata_did.patched_protocols.issue_credential.v1_0.messages',
 'peopledata_did.patched_protocols.issue_credential.v1_0.messages.inner',
 'peopledata_did.patched_protocols.issue_credential.v1_0.models',
 'peopledata_did.patched_protocols.present_proof',
 'peopledata_did.patched_protocols.present_proof.v1_0',
 'peopledata_did.patched_protocols.present_proof.v1_0.handlers',
 'peopledata_did.patched_protocols.present_proof.v1_0.messages',
 'peopledata_did.patched_protocols.present_proof.v1_0.messages.inner',
 'peopledata_did.patched_protocols.present_proof.v1_0.models',
 'peopledata_did.patched_protocols.present_proof.v1_0.util',
 'peopledata_did.v1_0',
 'peopledata_did.v1_0.decorators',
 'peopledata_did.v1_0.handlers',
 'peopledata_did.v1_0.messages',
 'peopledata_did.v1_0.models',
 'peopledata_did.v1_0.models.exchange_records',
 'peopledata_did.v1_0.routes',
 'peopledata_did.v1_0.routes.maps',
 'peopledata_did.v1_0.routes.openapi',
 'peopledata_did.v1_0.utils',
 'peopledata_did.v1_0.utils.did',
 'peopledata_did.v1_0.utils.jsonld',
 'peopledata_did.v1_0.utils.wallet']

package_data = \
{'': ['*']}

install_requires = \
['MarkupSafe==2.0.1',
 'PyJWT>=2.4.0,<3.0.0',
 'acapy-patched==0.5.6.dev1',
 'dexa-sdk==0.1.9',
 'py-multibase>=1.0.3,<2.0.0',
 'py-solc-x>=1.1.1,<2.0.0',
 'python3-indy>=1.16.0,<2.0.0',
 'semver>=2.13.0,<3.0.0',
 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'acapy-peopledata-did',
    'version': '0.1.0',
    'description': 'ACA-Py plugin for MyData DID DIDComm protcol',
    'long_description': '# ACA-Py plugin for Peopledata DID DIDComm protcol\n\n## ACA-Py Version Compatibility\n\nThis plugin is compatible with ACA-Py version 0.5.6.\n\n## Installation\n\nRequirements:\n- Python 3.6 or higher\n- ACA-Py 0.5.6\n\n### Setup Aries Cloud Agent - Python\n\nIf you already have an existing installation of ACA-Py, you can skip these steps\nand move on to [plugin installation](#plugin-installation). It is also worth\nnoting that this is not the only way to setup an ACA-Py instance. For more setup\nconfigurations, see the [Aries Cloud Agent - Python\nrepository](https://github.com/hyperledger/aries-cloudagent-python).\n\nFirst, prepare a virtual environment:\n```sh\n$ python3 -m venv env\n$ source env/bin/activate\n```\n\nInstall ACA-Py 0.5.6 into the virtual environment:\n```sh\n$ pip install aries-cloudagent==0.5.6\n```\n\n### Plugin Installation\n\nInstall this plugin into the virtual environment:\n\n```sh\n$ pip install acapy-peopledata-did\n```\n\n**Note:** Depending on your version of `pip`, you may need to drop or add \n`#egg=peopledata_did` to install the plugin with the above command.\n\n### Plugin Loading\nStart up ACA-Py with the plugin parameter:\n```sh\n$ aca-py start \\\n    -it http 0.0.0.0 8002 \\\n    -ot http \\\n    -e "http://localhost:8002/" \\\n    --label "Agent" \\\n    --admin 0.0.0.0 8001 \\\n    --admin-insecure-mode \\\n    --auto-accept-requests \\\n    --auto-ping-connection \\\n    --auto-respond-credential-offer \\\n    --auto-respond-credential-request \\\n    --auto-store-credential \\\n    --auto-respond-presentation-proposal \\\n    --auto-respond-presentation-request \\\n    --auto-verify-presentation \\\n    --genesis-url https://indy.igrant.io/genesis \\\n    --wallet-type indy \\\n    --wallet-name "agent_wallet" \\\n    --log-level info \\\n    --wallet-key "wallet@123" \\\n    --plugin "Peopledata_did"\n```\n\n## Licensing\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.\n\nYou may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.\n\n',
    'author': 'jerry zhang',
    'author_email': 'jerry.zhang.bill@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/decentralised-dataexchange/acapy-mydata-did-protocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
