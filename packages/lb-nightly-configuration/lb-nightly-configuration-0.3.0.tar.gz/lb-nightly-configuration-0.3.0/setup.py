# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb', 'lb.nightly.configuration']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'configurator>=2.6.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'graph': ['networkx>=2.6.1,<3.0.0']}

entry_points = \
{'console_scripts': ['lbn-check-config = '
                     'lb.nightly.configuration:check_config']}

setup_kwargs = {
    'name': 'lb-nightly-configuration',
    'version': '0.3.0',
    'description': 'classes and functions to suppot the LHCb Nightly Build System configuration',
    'long_description': 'None',
    'author': 'Marco Clemencic',
    'author_email': 'marco.clemencic@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
