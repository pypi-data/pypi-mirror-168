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
    'version': '0.0.3',
    'description': 'CLI application for managing AWS Control Tower for your AWS Organization.',
    'long_description': '# ctower\nControl Tower CLI application.\n\n## Poetry\n```bash\npoetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD\n```\n\n```bash\npip install ctower\nctower apply strongly-recommended\n```\n\n## Tasks\n- upload to pypi\n- logic for enabling controls\n    - enable singular control to ou\n    - sync one account to other\n        - --strict to mirror the controls\n        - nothing to just merge apply \n- ? maybe prompting\n- show accounts under ous\n- ',
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
