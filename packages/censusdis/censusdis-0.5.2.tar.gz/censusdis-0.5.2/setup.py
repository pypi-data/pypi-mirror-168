# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['censusdis']

package_data = \
{'': ['*']}

install_requires = \
['Rtree>=1.0.0,<2.0.0',
 'divintseg>=0.2.0,<0.3.0',
 'geopandas>=0.11.1,<0.12.0',
 'geopy>=2.2.0,<3.0.0',
 'matplotlib>=3.5.3,<4.0.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=5.1.1,<6.0.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinxcontrib-napoleon==0.7']}

setup_kwargs = {
    'name': 'censusdis',
    'version': '0.5.2',
    'description': 'US Census utilities for a variety of data loading and mapping purposes.',
    'long_description': "# censusdis\n\n[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)\n\n## Introduction \n\n`censusdis` is a package for discovering, loading, analyzing, and computing\ndiversity, integration, and segregation metrics\nto U.S. Census demographic data. \n\nIt can be installed in any python 3.9+ virtual environment using\n\n```shell\npip install censusdis\n```\n\n## Modules\n\nThe modules that make up the `censusdis` package are\n\n| Module                | Description                                                                |\n|-----------------------|:---------------------------------------------------------------------------|\n| `censusdis.geography` | Code for managing geography hierarchies in which census data is organized. | \n| 'censusdis.data`      | Code for fetching data from the US Census API, including managing datasets, groups, and variable hierarchies. |\n| `censusdis.maps`      | Code for downloading map data from the US, caching it locally, and using it to render maps. |\n| `censusdis.states`    | Constants defining the US States. Used by the three other modules. |\n\n## Demonstration Notebooks\n\nThere are several demonstration notebooks avaialable to illustrate how `censusdis` can\nbe used. They are found in the \n[notebook](https://github.com/vengroff/censusdis/tree/main/notebooks) \ndirectory of the source code.\n\nThe notebooks include\n\n| Notebook Name                                                                                                      | Description                                                                                                                                                         |\n|--------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| [SoMa DIS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/SoMa%20DIS%20Demo.ipynb)           | Load race and ethhicity data for two twons in Essex County, NJ and compute diversity and integration metrics.                                                       |\n| [ACS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/ACS%20Demo.ipynb)                       | Load American Community Survey (ACS) data for New Jersey and plot diversity statewide at the census block group level.                                              |\n| [Seeing White.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Seeing%20White.ipynb)               | Load nationwide demographic data at the county level and plot of map of the US showing the percent of the population wh identify as white only at the county level. | \n| [Map Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Map%20Demo.ipynb)                       | Demonstrate loading at plotting maps of New Jersey at different geographic granularity.                                                                             |\n| [Exploring Variables.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Exploring%20Variables.ipynb) | Load metatdata on a group of variables, visualize the tree hierarchy of variables in the group, and load data from the leaves of the tree.                          |\n\n\n## Diversity and Integration Metrics\n\nDiversity and integration metrics from the `divintseg` package are \ndemonstrated in some of the notebooks.\n\nFor more information on these metrics\nsee the [divintseg](https://github.com/vengroff/divintseg/) \nproject.\n\n",
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
