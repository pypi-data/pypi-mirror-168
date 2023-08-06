# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyveb']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.24.24',
 'numpy==1.21.2',
 'pandas==1.3.2',
 'psutil>=5.9.0,<6.0.0',
 'psycopg2-binary==2.9.1',
 'pyarrow==5.0.0',
 'pyodbc==4.0.30',
 'pyspark>=3.0.0,<4.0.0',
 'pyyaml==6.0',
 'requests==2.27.1',
 's3fs==0.4.2',
 'selenium==3.141.0',
 'simple-ddl-parser==0.26.5',
 'webdriver-manager==3.4.1']

setup_kwargs = {
    'name': 'pyveb',
    'version': '0.1.28',
    'description': 'Package containing common code and reusable components for pipelines and dags',
    'long_description': '# General \n\nPackage containing resuable code components for data pipelines and dags deployed to pypi.\n\n# Usage\n\n- Install/Upgrade locally: \n\n$ pip3 install pyveb\n$ pip3 install pyveb --upgrade\n\n- Import\n\nimport pyveb\nfrom pyveb import selenium_client\n\n\n# Update package\n\nUpload package: https://packaging.python.org/en/latest/tutorials/packaging-projects/ \n\n1.  update version in ~/pyproject.toml\n2.  deploy to pypi\n\n\nTBD \n\nWe bump the version automatically within the github action and commit the changes back to the branch\n\n    - $ rm -rf dist\n    - $ poetry\n    - $ python3 -m twine upload dist/*\n    - $ rm -rf dist\n\n3.  provide username and password of AWS SSM prd/pypi at prompt\n\nCredentials test: AWS SSM - test/pypi\nCredentials PRD: AWS SSM - prd/pypi\n\nusername: veb_prd_user\npassword: *****\n\n\n\n\n\n\n\n\n\n',
    'author': 'pieter',
    'author_email': 'pieter.de.petter@veb.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
