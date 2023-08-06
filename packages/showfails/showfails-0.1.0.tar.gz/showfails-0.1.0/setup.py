# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['showfails']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['showfails = showfails.__main__:cli']}

setup_kwargs = {
    'name': 'showfails',
    'version': '0.1.0',
    'description': '',
    'long_description': '# showfails\nparse junit style result.xml files and summarize failures and errors\n',
    'author': 'dskard',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
