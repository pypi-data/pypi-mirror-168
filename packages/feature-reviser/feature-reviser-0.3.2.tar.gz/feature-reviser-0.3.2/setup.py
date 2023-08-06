# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feature_reviser',
 'feature_reviser.feature_selection',
 'feature_reviser.transformer']

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
    'version': '0.3.2',
    'description': 'Find the right features of your dataset for the right model.',
    'long_description': '![The machine](https://raw.githubusercontent.com/chrislemke/feature-reviser/master/assets/machine.png)\n\n# feature-reviser\n\n[![tests](https://img.shields.io/github/workflow/status/chrislemke/feature-reviser/testing?label=tests&logo=github)](https://github.com/chrislemke/feature-reviser/actions/workflows/testing.yml)\n[![build](https://img.shields.io/github/workflow/status/chrislemke/feature-reviser/deploy_package?logo=github)](https://github.com/chrislemke/feature-reviser/actions/workflows/deploy_package.yml)\n[![python version](https://img.shields.io/pypi/pyversions/feature-reviser?logo=python&logoColor=yellow)](https://www.python.org/)\n[![release](https://img.shields.io/github/v/release/chrislemke/feature-reviser?include_prereleases)](https://github.com/chrislemke/feature-reviser/releases)\n[![pypi](https://img.shields.io/pypi/v/feature-reviser)](https://pypi.org/project/feature-reviser/)\n[![license](https://img.shields.io/github/license/chrislemke/feature-reviser)](https://github.com/chrislemke/feature-reviser/blob/main/LICENSE)\n## Introduction\nThe feature-reviser makes it easier to find the right features for a classifier.\nAfter creating different features, the question often arises whether they improve or worsen the performance of the classifier and thus have a direct positive or negative influence on the prediction. This project is intended to simplify the selection of features and at the same time contribute to simplifying and automating the entire processing process.\n\nAdditionally, this project also contains feature engineering steps, which can be used in a [Scikit-Learn pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html). Check out the [`custom_transformer`](https://github.com/chrislemke/feature-reviser/blob/main/feature_reviser/transformer/custom_transformer.py) module for more information.\n\n## Installation\nIf you are using [Poetry](https://python-poetry.org/), you can install the package with the following command:\n```bash\npoetry add feature-reviser\n```\nIf you are using [pip](https://pypi.org/project/pip/), you can install the package with the following command:\n```bash\npip install feature-reviser\n```\n\n## installing dependencies\nWith [Poetry](https://python-poetry.org/):\n```bash\npoetry install\n```\nWith [pip](https://pypi.org/project/pip/):\n```bash\npip install -r requirements.txt\n```\n\n## Further information\nFor further information, please refer to the [documentation](https://chrislemke.github.io/feature-reviser/).\n',
    'author': 'Christopher Lemke',
    'author_email': 'chris@syhbl.mozmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chrislemke/feature-reviser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
