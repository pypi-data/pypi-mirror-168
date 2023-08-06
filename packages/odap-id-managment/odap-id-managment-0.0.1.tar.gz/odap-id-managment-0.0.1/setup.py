# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['idsmanagment', 'idsmanagment.samId', 'idsmanagment.test']

package_data = \
{'': ['*'], 'idsmanagment': ['_config/*']}

install_requires = \
['daipe-core>=1.4.2,<2.0.0',
 'databricks-bundle>=1.4.12,<2.0.0',
 'pyfony-bundles>=0.4.4,<0.5.0']

entry_points = \
{'pyfony.bundle': ['create = idsmanagment.IdsManagment:IdsManagment']}

setup_kwargs = {
    'name': 'odap-id-managment',
    'version': '0.0.1',
    'description': 'IDs managment for ODAP',
    'long_description': '# IDs Managment\n\n**This package is distributed under the "DataSentics SW packages Terms of Use." See [license](https://raw.githubusercontent.com/DataSentics/odap-id-managment/master/LICENSE)**\n\nIDs managment provides algorithms for combining different IDs into one master user ID.  \n',
    'author': 'Datasentics',
    'author_email': 'samuel.bajanik@datasentics.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DataSentics/odap-id-managment',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
