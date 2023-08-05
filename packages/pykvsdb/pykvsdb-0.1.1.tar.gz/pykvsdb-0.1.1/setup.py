# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['pykvsdb']
setup_kwargs = {
    'name': 'pykvsdb',
    'version': '0.1.1',
    'description': 'A key-value store database written from the ground-up with speed in mind.',
    'long_description': '# PYKVSDB\nA key-value store database written from the ground-up with speed in mind.\n\n## Installation\nPYKVSDB can be installed via pip:\n\n```pip install pykvsdb```\n\n## Syntax\n### Setting Values\nYou can store a key-value pair in PYKVSDB with the ```set``` function:\n\n```pykvsdb.set("language", "python")```\n### Getting Values\nTo retrieve a value, use the ```get``` function:\n\n```pykvsdb.get("language")```\n\n### Saving to the file system\nIf you would like to be able to access your data later you will need to save it to the file system with ```save```:\n\n```pykvsdb.save("test.db")```\n\n### Loading a saved database\nIf you need to access a database saved to the file system again, you need to load it with ```load```:\n\n```pykvsdb.load("test.db")```\n',
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
