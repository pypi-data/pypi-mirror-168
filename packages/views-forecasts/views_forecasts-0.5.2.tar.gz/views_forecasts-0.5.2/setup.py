# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['views_forecasts']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>3.4.5,<40.0.0',
 'numpy>=1.20,<2.0',
 'pandas>=1.2.3,<2.0.0',
 'psycopg2>=2.8.1,<3.0.0',
 'python-dotenv>=0.18,<0.19',
 'sqlalchemy>=1.3,<2.0',
 'views-runs>=1.13.1,<2.0.0',
 'views-storage>=1.1.4,<2.0.0',
 'viewser>=5.13.0,<6.0.0']

setup_kwargs = {
    'name': 'views-forecasts',
    'version': '0.5.2',
    'description': 'Forecast store for ViEWS3.',
    'long_description': '# Predictions management system for viewser.\n',
    'author': 'Mihai Croicu',
    'author_email': 'mihai.croicu@pcr.uu.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UppsalaConflictDataProgram/views_forecasts>',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
