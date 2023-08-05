# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiop4']

package_data = \
{'': ['*']}

install_requires = \
['googleapis-common-protos==1.54.0',
 'grpcio==1.46.3',
 'p4runtime==1.4.0rc5',
 'protobuf==3.18.1']

setup_kwargs = {
    'name': 'aiop4',
    'version': '0.2.0',
    'description': 'asyncio P4Runtime Python client',
    'long_description': '<div align="center">\n  <h1><code>aiop4</code></h1>\n\n  <strong>asyncio P4Runtime Python client</strong>\n\n  <p></p>\n  <p>\n    <a href="https://github.com/viniarck/aiop4/actions/workflows/unit-tests.yml/badge.svg?branch=main"><img src="https://github.com/viniarck/aiop4/actions/workflows/unit-tests.yml/badge.svg?branch=main" alt="tests" /></a>\n    <a href="https://pypi.org/project/aiop4/"><img src="https://img.shields.io/pypi/v/aiop4" alt="aiop4 pypi" /></a>\n    <a href="https://img.shields.io/pypi/pyversions/aiop4"><img src="https://img.shields.io/pypi/pyversions/aiop4" alt="aiop4 py versions" /></a>\n    <a href="https://img.shields.io/badge/status-experimental-yellow"><img src="https://img.shields.io/badge/status-experimental-yellow" alt="aiop4 py versions" /></a>\n  </p>\n\n</div>\n\n## aiop4\n\n`aiop4` is an `asyncio` client for [P4Runtime](https://github.com/p4lang/p4runtime/blob/v1.3.0/proto/p4/v1/p4runtime.proto). Breaking changes will likely happen until v1 is released.\n\n## How to install\n\n- `poetry add aiop4` or `pip install aiop4`\n\n## Examples\n\n- [L2 learning switch](./examples/l2_switch/l2_switch_app.py)\n',
    'author': 'Vinicius Arcanjo',
    'author_email': 'viniarck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/viniarck/aiop4',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
