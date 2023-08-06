# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numalogic',
 'numalogic.models',
 'numalogic.models.autoencoder',
 'numalogic.models.autoencoder.variants',
 'numalogic.models.forecast',
 'numalogic.models.forecast.variants',
 'numalogic.preprocess',
 'numalogic.registry',
 'numalogic.synthetic',
 'numalogic.tests',
 'numalogic.tests.models',
 'numalogic.tests.models.autoencoder',
 'numalogic.tests.models.autoencoder.variants',
 'numalogic.tests.models.forecast',
 'numalogic.tests.preprocess',
 'numalogic.tests.registry',
 'numalogic.tests.synthetic',
 'numalogic.tests.tools',
 'numalogic.tools']

package_data = \
{'': ['*'], 'numalogic.tests': ['resources/data/*']}

install_requires = \
['mlflow-skinny>=1.27.0,<2.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pytz>=2022.1,<2023.0',
 'scikit-learn>=1.0,<2.0',
 'torch>=1.12.0,<2.0.0',
 'torchinfo>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'numalogic',
    'version': '0.2.4',
    'description': 'Collection of operational Machine Learning models and tools.',
    'long_description': '# numalogic\n\n[![Build](https://github.com/numaproj/numalogic/actions/workflows/ci.yml/badge.svg)](https://github.com/numaproj/numalogic/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/numaproj/numalogic/branch/main/graph/badge.svg?token=020HF97A32)](https://codecov.io/gh/numaproj/numalogic)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\nNumalogic is a collection of ML models and algorithms for operation data analytics and AIOps. At Intuit, we use Numalogic at scale for continuous real-time data enrichment including anomaly scoring. We assign an anomaly score (ML inference) to any time-series datum/event/message we receive on our streaming platform (say, Kafka). 95% of our data sets are time-series, and we have a complex flowchart to execute ML inference on our high throughput sources. We run multiple models on the same datum, say a model that is sensitive towards +ve sentiments, another more tuned towards -ve sentiments, and another optimized for neutral sentiments. We also have a couple of ML models trained for the same data source to provide more accurate scores based on the data density in our model store. An ensemble of models is required because some composite keys in the data tend to be less dense than others, e.g., forgot-password interaction is less frequent than a status check interaction. At runtime, for each datum that arrives, models are picked based on a conditional forwarding filter set on the data density. ML engineers need to worry about only their inference container; they do not have to worry about data movement and quality assurance.\n\n## Numalogic realtime training \nFor an always-on ML platform, the key requirement is the ability to train or retrain models automatically based on the incoming messages. The composite key built at per message runtime looks for a matching model, and if the model turns out to be stale or missing, an automatic retriggering is applied. The conditional forwarding feature of the platform improves the development velocity of the ML developer when they have to make a decision whether to forward the result further or drop it after a trigger request.\n\n\n## Installation\n\n```shell\npip install numalogic\n```\n\n\n## Develop locally\n\n1. Install Poetry:\n    ```\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -\n    ```\n2. To activate virtual env:\n    ```\n    poetry shell\n    ```\n3. To install all dependencies: ( listed on pyproject.toml)\n   ```\n   make setup\n   ```\n4. To install dependencies:\n    ```\n    poetry install\n    ```\n5. To run tests with coverage:\n    ```\n    make test\n    ```\n6. To format code style using black:\n    ```\n    make format\n    ```\n',
    'author': 'Numalogic Developers',
    'author_email': 'None',
    'maintainer': 'Avik Basu',
    'maintainer_email': 'avikbasu93@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
