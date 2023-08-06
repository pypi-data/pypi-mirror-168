# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feature_reviser']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'feature-reviser',
    'version': '0.1',
    'description': 'Find the right features of your dataset for the right model.',
    'long_description': 'None',
    'author': 'Christopher Lemke',
    'author_email': 'chris@syhbl.mozmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chrislemke/feature-reviser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
