# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raplan']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'plotly>=5.7.0,<6.0.0', 'pyserde[yaml]>=0.9.2,<0.10.0']

extras_require = \
{'plot': ['kaleido==0.2.1']}

setup_kwargs = {
    'name': 'raplan',
    'version': '0.2.0',
    'description': 'Ratio planning and scheduling in Python.',
    'long_description': 'None',
    'author': 'Ratio Innovations B.V.',
    'author_email': 'info@ratio-case.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/ratio-case/python/raplan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
