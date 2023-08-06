# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_logging_end_to_end_test_tool']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=14.0.0,<15.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'PyYAML>5.0,<7',
 'pytest>=7.1.2,<8.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'pytest11': ['plugin = pytest_logging_end_to_end_test_tool.plugin']}

setup_kwargs = {
    'name': 'pytest-logging-end-to-end-test-tool',
    'version': '1.0.7',
    'description': '',
    'long_description': None,
    'author': 'Ryan Faircloth',
    'author_email': 'ryan@dss-i.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
