# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mundipy', 'mundipy.api', 'mundipy.pcs']

package_data = \
{'': ['*']}

install_requires = \
['Fiona>=1.8.21,<2.0.0',
 'Shapely>=1.8.4,<2.0.0',
 'geopandas>=0.11.1,<0.12.0',
 'matplotlib>=3.6.0,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'overpy>=0.6,<0.7',
 'pandas>=1.5.0,<2.0.0',
 'pygeos>=0.13,<0.14',
 'pyproj>=3.4.0,<4.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'mundipy',
    'version': '0.1.0',
    'description': 'mundipy is a Python framework for spatial data analysis',
    'long_description': "# ![mundi.py](docs/logo/light.svg)\n\n[![PyPI version](https://badge.fury.io/py/mundipy.svg)](https://pypi.org/project/mundipy/)\n\nmundipy is a Python framework for spatial data manipulation. Built on top of\n[geopandas](https://geopandas.org/en/stable/), [GDAL](https://gdal.org/),\nand [shapely](https://shapely.readthedocs.io/en/stable/manual.html), mundi.py\nprovides a useful abstraction to eliminate the hassles of spatial data.\n\n## Projected Coordinate Systems\n\nAutomatically suggests a projected coordinate system to use, given a shapely\ngeometry in WGS84.\n\nThis prioritizes coordinate systems that:\n1. totally contain the given geometry\n2. have minimal area (probably less distortion)\n3. are not deprecated\n\n```py\n>>> from mundipy.pcs import choose_pcs\n>>> from shapely.geometry import Point\n\n>>> choose_pcs(Point(-118.24, 34.052), units='feet')\n{\n    'name': 'NAD27 / California zone VII',\n    'epsg': 26799,\n    'crs': 'EPSG:26799',\n    'units': 'feet'\n}\n```\n\n## Project Roadmap\n\n- No projections needed: automatically chooses and selects a relevant CRS when doing operations\n- Automatic spatial indexing\n- Jupyter notebook native (\\_repr\\_html\\_) that doesn't explode with massive data\n- Nearest neighbor/distance queries\n- Spatial joins\n- Dissolving into h3/s2\n\n## License\n\nMundi.py is MIT licensed.\n",
    'author': 'Brendan Ashworth',
    'author_email': 'brendan@buntinglabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://buntinglabs.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
