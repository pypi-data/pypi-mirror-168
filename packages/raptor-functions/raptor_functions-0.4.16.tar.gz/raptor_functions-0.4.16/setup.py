# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raptor_functions',
 'raptor_functions.eda',
 'raptor_functions.examples.bosch_data',
 'raptor_functions.examples.daniel_examples.pigs_data',
 'raptor_functions.semi_supervised',
 'raptor_functions.semi_supervised.copkmeans',
 'raptor_functions.supervised',
 'raptor_functions.unsupervised']

package_data = \
{'': ['*'],
 'raptor_functions': ['ensemble/*',
                      'examples/*',
                      'examples/daniel_examples/*',
                      'examples/daniel_examples/air_freshener/*',
                      'examples/daniel_examples/semi_supervised/*',
                      'examples/daniel_examples/sensor_visualisations/*',
                      'examples/dashboard/*',
                      'examples/plots/*',
                      'examples/ssc/*',
                      'nn/*',
                      'rapmon/*'],
 'raptor_functions.examples.bosch_data': ['dashboard/*',
                                          'figures/*',
                                          'output/*'],
 'raptor_functions.examples.daniel_examples.pigs_data': ['dashboard/*']}

install_requires = \
['Boruta==0.3',
 'boto3==1.21.35',
 'explainerdashboard==0.3.5',
 'joblib==1.0.1',
 'matplotlib==3.5.1',
 'mlflow==1.24.0',
 'numpy>=1.21.0,<2.0.0',
 'optuna==2.10.0',
 'pandas==1.3.5',
 'pycaret==2.3.9',
 'python-decouple==3.6',
 'python-dotenv==0.20.0',
 'scikit-learn==0.23.2',
 'scipy==1.5.4',
 'tsfresh==0.19.0',
 'xgboost==1.5.2']

setup_kwargs = {
    'name': 'raptor-functions',
    'version': '0.4.16',
    'description': '',
    'long_description': None,
    'author': 'Ibrahim',
    'author_email': 'iaanimashaun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.9',
}


setup(**setup_kwargs)
