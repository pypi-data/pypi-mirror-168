# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scikit_tab_trans']

package_data = \
{'': ['*']}

install_requires = \
['headers_workaround>=0.18,<0.19',
 'joblib>=1.2.0,<2.0.0',
 'pytorch-widedeep>=1.2.0,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'scikit-tabtrans',
    'version': '0.1',
    'description': 'TabTransformer ready for Scikit learn.',
    'long_description': None,
    'author': 'Christopher Lemke',
    'author_email': 'chris.lemke@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrislemke/scikit-TabTrans',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
