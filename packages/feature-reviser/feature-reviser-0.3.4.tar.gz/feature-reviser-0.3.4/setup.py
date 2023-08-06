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
 'phonenumbers>=8.12.56,<9.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'sklearn-pandas>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'feature-reviser',
    'version': '0.3.4',
    'description': 'Construct and find the right features of your dataset for the right model.',
    'long_description': "![The machine](https://raw.githubusercontent.com/chrislemke/feature-reviser/master/assets/machine.png)\n\n# feature-reviser\n\n[![test suite](https://img.shields.io/github/workflow/status/chrislemke/feature-reviser/testing?label=tests&logo=github)](https://github.com/chrislemke/feature-reviser/actions/workflows/testing.yml)\n[![build](https://img.shields.io/github/workflow/status/chrislemke/feature-reviser/deploy_package?logo=github)](https://github.com/chrislemke/feature-reviser/actions/workflows/deploy_package.yml)\n[![python version](https://img.shields.io/pypi/pyversions/feature-reviser?logo=python&logoColor=yellow)](https://www.python.org/)\n[![release](https://img.shields.io/github/v/release/chrislemke/feature-reviser?include_prereleases)](https://github.com/chrislemke/feature-reviser/releases)\n[![pypi](https://img.shields.io/pypi/v/feature-reviser)](https://pypi.org/project/feature-reviser/)\n[![license](https://img.shields.io/github/license/chrislemke/feature-reviser)](https://github.com/chrislemke/feature-reviser/blob/main/LICENSE)\n## Introduction\nThe feature-reviser makes it easier to construct and find the right features for a classifier.\n\nIn this project, we want to conquer two big challenges in the field of machine learning/data science: feature engineering and feature selection.\n\nEvery data is different every column needs to be treated differently. So one part of this project is a [collection of various transformers](https://github.com/chrislemke/feature-reviser/tree/main/feature_reviser/transformer) that can be used for preprocessing. Because even if columns are somehow always different, some patterns can be generalized. We believe, that a brought collection of preprocessing transformers is like a well-equipped toolbox: You always find the tool you need and sometimes you get inspired by seeing a tool you did not recognize before. BTW: Feel free to contribute to this toolbox.\n\nOnce you have a set of features, you need to find the right ones. This is where the feature selection comes in. We want to provide a collection of feature selection algorithms to quickly find your best collection. The main idea is that this process should be automated. Because there are better things to do in life than trying out different feature combinations. \U0001f6dd Check out [Scikit-learn's feature selection](https://scikit-learn.org/stable/modules/classes.html?highlight=feature+selection#module-sklearn.feature_selection) module and the options [feature-engine](https://feature-engine.readthedocs.io/en/latest/api_doc/selection/index.html) for great already existing implementations.\n\n\n## Installation\nIf you are using [Poetry](https://python-poetry.org/), you can install the package with the following command:\n```bash\npoetry add feature-reviser\n```\nIf you are using [pip](https://pypi.org/project/pip/), you can install the package with the following command:\n```bash\npip install feature-reviser\n```\n\n## installing dependencies\nWith [Poetry](https://python-poetry.org/):\n```bash\npoetry install\n```\nWith [pip](https://pypi.org/project/pip/):\n```bash\npip install -r requirements.txt\n```\n\n## Feature reviser\nFinding the best features for your model is hard. In the `feature_selection` part of the project, we try to automate this process to make it a bit easier. This part of the project is still in development and is not yet ready for use. 🚧 If you want to help, you can find more information in the [contributing guide](how_to_contribute.md).\n\n## The transformers\nData preprocessing often involves similar processes. No matter whether it is a matter of manipulating strings or numbers. [Scikit-learn's pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) implementation makes it easy to structure and sequence such preprocessing processes. To take advantage of this, the [`transformer`](https://github.com/chrislemke/feature-reviser/tree/main/feature_reviser/transformer) part of the project contains multiple modules including a set of transformers that can be easily pipelined to simplify preprocessing. The list of transformers is open and will be extended permanently.\n\n## Contributing\nWe're all kind of in the same boat. Preprocessing in data science is somehow very individual - every feature is different and must be handled and processed differently. But somehow we all have the same problems: sometimes date columns have to be changed. Sometimes strings have to be formatted, sometimes durations have to be calculated, etc. There is a huge number of preprocessing possibilities but we all use the same tools.\n\n[Scikit-learns pipelines](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) help to use formalized functions. So why not also share these so-called transformers with others? This open source project has the goal to collect useful preprocessing pipeline steps. Let us all collect what we used for preprocessing and share it with others. This way we can all benefit from each other's work and save a lot of time. So if you have a preprocessing step that you use regularly, please feel free to contribute it to this project. The idea is that this is not only a toolbox but also an inspiration for what is possible. Maybe you have not thought about this preprocessing step before.\n\nPlease check out the [documentation](how_to_contribute.md) on how to contribute to this project.\n\n\n## Further information\nFor further information, please refer to the [documentation](https://chrislemke.github.io/feature-reviser/).\n",
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
