# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctower']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.66,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'tabulate>=0.8.10,<0.9.0',
 'termcolor>=2.0.1,<3.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ctower = ctower.main:run_app']}

setup_kwargs = {
    'name': 'ctower',
    'version': '0.0.5',
    'description': 'CLI application for managing AWS Control Tower for your AWS Organization.',
    'long_description': '# ctower\n\nControl Tower CLI application.\n\n\n## Installation\n```bash\n# Make sure you have python:^3.7\npython3 --version\n\n# Install the PyPI package w/\npip3 install ctower\n\n# or\n\npython3 -m pip install ctower\n```\n## Poetry\n\n```bash\n\npoetry init\npoetry install\npoetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD\n\n# generate CLI application documentation\npoetry shell\ntyper ctower.main utils docs --name ctower --output CLI-README.md\n```\n\n```bash\npip install ctower\nctower apply strongly-recommended\n```\n\n## Tasks\n\n- logic for enabling controls\n  - enable singular control to ou\n  - sync one account to other\n    - --strict to mirror the controls\n    - nothing to just merge apply\n- ? maybe prompting\n- show accounts under ous\n-\n',
    'author': 'Oguzhan Yilmaz',
    'author_email': 'oguzhanylmz271@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kloia/ctower',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
