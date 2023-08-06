# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_dbt_artifacts', 'tap_dbt_artifacts.tests']

package_data = \
{'': ['*'], 'tap_dbt_artifacts': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['tap-dbt-artifacts = '
                     'tap_dbt_artifacts.tap:TapDbtArtifacts.cli']}

setup_kwargs = {
    'name': 'tap-dbt-artifacts',
    'version': '0.0.5',
    'description': '`tap-dbt-artifacts` is a Singer tap for dbt artifacts, built with the Meltano SDK for Singer Taps.',
    'long_description': 'None',
    'author': 'Prratek Ramchandani',
    'author_email': 'prratek.95@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
