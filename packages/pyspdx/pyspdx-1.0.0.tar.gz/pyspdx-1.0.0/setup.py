# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyspdx']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=3.0.9,<4.0.0']

setup_kwargs = {
    'name': 'pyspdx',
    'version': '1.0.0',
    'description': 'Validate SPDX expressions',
    'long_description': '# pyspdx\n\nShort library to validate SPDX expressions. I have not found any working implementation in python and I wanted to mess around with pyparsing anyways.\n\n## API / Usage\nThis lib only exposes one function:\n\n```\nfrom pyspdx import validate\n\nvalidate("MIT")  # Valid, does nothing\nvalidate("NotValid") # Throws ValueError\nvalidate("(Apache-2.0 OR MIT) AND BSD-3-Clause") # Valid\nvalidate("(DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2 OR (Apache-2.0 AND PostgreSQL OR OpenSSL)) AND (BSD-3-Clause OR Apache-2.0 WITH 389-exception)") # Valid\n```\n\n## Used Sources\n- https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/\n- https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html\n',
    'author': 'Tribe29 GmbH',
    'author_email': 'info@tribe29.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tribe29/pyspdx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
