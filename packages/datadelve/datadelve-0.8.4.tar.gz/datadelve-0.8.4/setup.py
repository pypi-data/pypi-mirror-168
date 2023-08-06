# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadelve']

package_data = \
{'': ['*']}

install_requires = \
['jsonpointer>=2.0,<3.0']

setup_kwargs = {
    'name': 'datadelve',
    'version': '0.8.4',
    'description': 'A library to read and manipulate nested data structures, particularly ones read from JSON files',
    'long_description': '# DataDelve\n[![PyPI version](https://badge.fury.io/py/datadelve.svg)](https://badge.fury.io/py/datadelve)\n[![Coverage Status](https://coveralls.io/repos/github/the-nick-of-time/datadelve/badge.svg?branch=master)](https://coveralls.io/github/the-nick-of-time/datadelve?branch=master)\n[![Build Status](https://travis-ci.org/the-nick-of-time/datadelve.svg?branch=master)](https://travis-ci.org/the-nick-of-time/datadelve)\n\nWorking with complex nested data can be tedious. If you have to access any objects that are four layers deep in a JSON response from a web service, you quickly tire of writing square brackets.\nMuch better would be to have a simple way of accessing data through a simple syntax. \n[jsonpointer](https://tools.ietf.org/html/rfc6901) is a perfect match, it looks just like paths through a filesystem.\nApplying this information to the data structures makes it easy and convenient.\n\n## Usage\n\n```python\nfrom datadelve import DataDelver\n\ndata = ["your annoying data here"]\ndelver = DataDelver(data)\nelement = delver.get("/dict/keys/and/1/list/index")\nsubset = delver.cd("/particular/key/to/focus/on")\ndelver.set("/path/to/change", "new")\ndelver.delete("/bad")\n```\n\n## Support\n\nThis package grew around a series of JSON files, so that is the primary focus. It therefore\nexpects data structures with dicts and lists. As the implementation is turned over to\njsonpointer, it will work for anything that implements `__getitem__(str)` or that is registered\nas a `collections.abc.Sequence` and implements `__getitem__(int)`.\n\nRaw data, loaded from whatever source, is accepted. So are JSON files. These have the added\nbenefit of being flyweight instances, so all views on the same file reference the same object.\nThis way none of them can get out of sync and make writes indeterminate as to what updates have\nactually been made. As YAML isn\'t in the standard library, I\'ve split support for that into a\nseparate project: [datadelve_yaml](https://pypi.org/project/datadelve_yaml/). YAML files are\ntreated the same as JSON.',
    'author': 'Nick Thurmes',
    'author_email': 'nthurmes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
