# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feature_reviser', 'feature_reviser.transformer']

package_data = \
{'': ['*']}

install_requires = \
['feature-engine>=1.4.1,<2.0.0',
 'joblib>=1.2.0,<2.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'sklearn-pandas>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'feature-reviser',
    'version': '0.2',
    'description': 'Find the right features of your dataset for the right model.',
    'long_description': 'None',
    'author': 'Christopher Lemke',
    'author_email': 'chris@syhbl.mozmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://chrislemke.github.io/feature-reviser/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
