# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bacorakel']

package_data = \
{'': ['*'], 'bacorakel': ['assets/*']}

install_requires = \
['CherryPy>=18.8.0,<19.0.0',
 'click>=8.1.3,<9.0.0',
 'dash-bootstrap-components>=1.2.1,<2.0.0',
 'dash-daq>=0.5.0,<0.6.0',
 'dash>=2.6.1,<3.0.0',
 'pyFirmata>=1.1.0,<2.0.0',
 'pyserde>=0.9.2,<0.10.0',
 'pyserial>=3.5,<4.0',
 'tomli-w>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['bacorakel = bacorakel.cli:bacorakel']}

setup_kwargs = {
    'name': 'bacorakel',
    'version': '0.0.56',
    'description': 'BACorakel service.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
