# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nysmix',
 'nysmix.cache',
 'nysmix.config',
 'nysmix.database',
 'nysmix.pipeline',
 'nysmix.store']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.27,<2.0.0',
 'joblib>=1.1.0,<2.0.0',
 'joblibgcs>=0.2.0,<0.3.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.10.1,<2.0.0']

extras_require = \
{'api': ['fastapi>=0.79.0,<0.80.0', 'uvicorn[standard]>=0.18.2,<0.19.0'],
 'book': ['jupyter-book>=0.13.0,<0.14.0',
          'jupytext>=1.14.0,<2.0.0',
          'altair>=4.2.0,<5.0.0',
          'autodocsumm>=0.2.8,<0.3.0'],
 'google': ['google-cloud-storage>=2.3.0,<3.0.0',
            'google-auth>=2.6.6,<3.0.0',
            'sqlalchemy-bigquery>=1.4.4,<2.0.0'],
 'test': ['pytest>=7.1.2,<8.0.0']}

setup_kwargs = {
    'name': 'nysmix',
    'version': '0.4.0',
    'description': 'pulling nys fuel mix data from nysiso',
    'long_description': None,
    'author': 'Gautam Sisodia',
    'author_email': 'gautam.sisodia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
