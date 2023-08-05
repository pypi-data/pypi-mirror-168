# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['censusdis']

package_data = \
{'': ['*']}

install_requires = \
['Rtree>=1.0.0,<2.0.0',
 'divintseg>=0.1.3,<0.2.0',
 'geopandas>=0.11.1,<0.12.0',
 'matplotlib>=3.5.3,<4.0.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=5.1.1,<6.0.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinxcontrib-napoleon==0.7']}

setup_kwargs = {
    'name': 'censusdis',
    'version': '0.4.1',
    'description': 'US Census utilities for a variety of data loading and mapping purposes.',
    'long_description': '# censusdis\n\nA package for applying diversity, integration, and segregation metrics\nto U.S. Census demographic data. See the [divintseg](https://github.com/vengroff/divintseg/) \nproject for more information on these metrics.\n\n[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)\n',
    'author': 'vengroff',
    'author_email': 'vengroff@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vengroff/censusdis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
