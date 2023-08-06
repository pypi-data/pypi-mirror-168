# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quantpiler']

package_data = \
{'': ['*']}

install_requires = \
['qiskit>=0.38.0,<0.39.0']

setup_kwargs = {
    'name': 'quantpiler',
    'version': '0.1.7',
    'description': 'Quantum compiler and common circuits library',
    'long_description': '[![License](https://img.shields.io/github/license/averyanalex/quantpiler.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Test](https://github.com/averyanalex/quantpiler/actions/workflows/test.yml/badge.svg)](https://github.com/averyanalex/quantpiler/actions/workflows/test.yml)\n[![Version](https://img.shields.io/pypi/v/quantpiler.svg)](https://pypi.org/project/quantpiler/)\n[![Docs](https://img.shields.io/readthedocs/quantpiler.svg)](https://quantpiler.readthedocs.io/en/latest/)\n\n# Quantpiler\n\nThis library was created to simplify the development of complex quantum algorithms by\nauto-generating common circuits and compiling python functions.\n\nDocumentation: [https://quantpiler.readthedocs.io/en/latest/index.html](https://quantpiler.readthedocs.io/en/latest/index.html)\n\nUsage examples: [https://quantpiler.readthedocs.io/en/latest/examples/index.html](https://quantpiler.readthedocs.io/en/latest/examples/index.html)\n',
    'author': 'AveryanAlex',
    'author_email': 'alex@averyan.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/averyanalex/quantpiler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
