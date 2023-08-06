# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jenfi_pipeline_data_app',
 'jenfi_pipeline_data_app.app_funcs',
 'jenfi_pipeline_data_app.config']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.40,<2.0.0',
 'boto3>=1.24.78,<2.0.0',
 'numpy>=1.23.2,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'psycopg2>=2.9.3,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['pipeline-data-app = pipeline_data_app:main']}

setup_kwargs = {
    'name': 'jenfi-pipeline-data-app',
    'version': '0.2.3',
    'description': '',
    'long_description': "# Jenfi Pipeline Data App\n\nDesigned to allow teams to access Jenfi's data sources in a Jupyter Notebook.\n\n## Usage\n\n```python\nfrom jenfi_pipeline_data_app import PipelineDataApp as Jenfi\n\nJenfi.ROOT_DIR # => /Your/app/root/dir\n```\n",
    'author': 'Justin Louie',
    'author_email': '224840+nitsujri@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
