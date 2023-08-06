# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helax', 'helax.jax', 'helax.numpy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.3,<2.0.0', 'scipy>=1.9.1,<2.0.0']

extras_require = \
{'gpu': ['jax>=0.3.17,<0.4.0', 'jaxlib>=0.3.15,<0.4.0', 'chex>=0.1.5,<0.2.0']}

setup_kwargs = {
    'name': 'helax',
    'version': '0.1.2',
    'description': 'Python package for computing helicity amplitudes',
    'long_description': '# `helax`: Helicity Amplitudes with Jax or NumPy\n\nImplementation from scratch of the HELAS library using Jax and NumPy.\n',
    'author': 'Logan A. Morrison',
    'author_email': 'loganmorrison99@gmail.com',
    'maintainer': 'Logan Morrison',
    'maintainer_email': 'loganmorrison99@gmail.com',
    'url': 'https://github.com/LoganAMorrison/helax',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
