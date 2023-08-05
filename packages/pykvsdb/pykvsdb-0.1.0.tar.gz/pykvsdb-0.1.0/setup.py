# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['pykvsdb']
setup_kwargs = {
    'name': 'pykvsdb',
    'version': '0.1.0',
    'description': 'A key-value store database written from the ground-up with speed in mind.',
    'long_description': '# PYKVSDB\nA key-value store database written from the ground-up with speed in mind.\n\n',
    'author': 'DrgnFireYellow',
    'author_email': '86269995+DrgnFireYellow@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
